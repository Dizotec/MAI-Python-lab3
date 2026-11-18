import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

import pytest

from src.catalog import Catalog
from src.detail import Detail
from src.errors import (
    CorruptedFileError,
    DuplicateIdError,
    UnsupportedFormatVersionError,
)
from src.storage import load_catalog, load_into_catalog, save_catalog


def test_storage(tmp_path: Path) -> None:
    catalog = Catalog()
    detail1 = Detail(
        "ART-0042", "Шестерня привода", "Механика", date(2026, 11, 12), 1.45, "Сталь"
    )
    detail2 = Detail(
        "ART-0043", "Шестерня ", "Гидравлика", date(2026, 11, 13), 1.5, "Медь"
    )
    catalog.add(detail1)
    catalog.add(detail2)
    path = tmp_path / "catalog.json"
    save_catalog(catalog, str(path))
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert data["format_version"] == 1
        assert len(data["items"]) == 2
        assert data["items"][0]["identifier"] == detail1.identifier
        assert data["items"][0]["name"] == detail1.name
        assert data["items"][0]["category"] == detail1.category
        assert data["items"][0]["date"] == detail1.date.isoformat()
        assert data["items"][0]["mass"] == detail1.mass
        assert data["items"][0]["material"] == detail1.material

        assert data["items"][1]["identifier"] == detail2.identifier
        assert data["items"][1]["name"] == detail2.name
        assert data["items"][1]["category"] == detail2.category
        assert data["items"][1]["date"] == detail2.date.isoformat()
        assert data["items"][1]["mass"] == detail2.mass
        assert data["items"][1]["material"] == detail2.material


def test_save_empty_catalog(tmp_path: Path) -> None:
    catalog = Catalog()
    path = tmp_path / "empty_catalog.json"

    save_catalog(catalog, str(path))

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["format_version"] == 1
    assert data["items"] == []


def test_save_preserves_original_data(tmp_path: Path) -> None:
    catalog = Catalog()
    detail1 = Detail(
        "ART-0042", "Шестерня привода", "Механика", date(2026, 11, 12), 1.45, "Сталь"
    )
    detail2 = Detail(
        "ART-0043", "Шестерня насоса", "Гидравлика", date(2026, 11, 13), 1.5, "Медь"
    )
    catalog.add(detail1)
    catalog.add(detail2)

    original1 = asdict(detail1)
    original2 = asdict(detail2)

    save_catalog(catalog, str(tmp_path / "catalog.json"))

    assert len(catalog) == 2
    assert list(catalog) == [detail1, detail2]
    assert catalog.get("ART-0042") is detail1
    assert catalog.get("ART-0043") is detail2

    assert asdict(detail1) == original1
    assert asdict(detail2) == original2
    assert isinstance(detail1.date, date)
    assert isinstance(detail2.date, date)


def test_catalog_json_round_trip(tmp_path: Path) -> None:
    catalog = Catalog()
    detail1 = Detail(
        "ART-0042",
        "Шестерня привода",
        "Механика",
        date(2026, 11, 12),
        1.45,
        "Сталь",
    )
    detail2 = Detail(
        "ART-0043",
        "Шестерня насоса",
        "Гидравлика",
        date(2026, 11, 13),
        1.5,
        "Медь",
    )
    catalog.add(detail1)
    catalog.add(detail2)

    path = tmp_path / "catalog.json"
    save_catalog(catalog, str(path))
    loaded = load_catalog(str(path))

    assert isinstance(loaded, Catalog)
    assert len(loaded) == 2
    assert list(loaded) == [detail1, detail2]
    assert isinstance(loaded.get("ART-0042").date, date)
    assert isinstance(loaded.get("ART-0043").date, date)


def test_load_empty_catalog(tmp_path: Path) -> None:
    catalog = Catalog()
    path = tmp_path / "empty_catalog.json"

    save_catalog(catalog, str(path))
    loaded = load_catalog(str(path))

    assert isinstance(loaded, Catalog)
    assert len(loaded) == 0


def test_load_corrupted_json(tmp_path: Path) -> None:
    path = tmp_path / "corrupted.json"
    with open(path, "w", encoding="utf-8") as file:
        file.write("{")
    with pytest.raises(CorruptedFileError):
        load_catalog(path)


def test_load_unsupported_version(tmp_path: Path) -> None:
    path = tmp_path / "corrupted.json"
    test_record = {"format_version": 99, "items": []}
    with open(path, "w", encoding="utf-8") as file:
        json.dump(test_record, file)
    with pytest.raises(UnsupportedFormatVersionError):
        load_catalog(path)


def test_load_invalid_mass(tmp_path: Path) -> None:
    catalog = Catalog()
    detail1 = Detail(
        "ART-0042",
        "Шестерня привода",
        "Механика",
        date(2026, 11, 12),
        1.45,
        "Сталь",
    )
    catalog.add(detail1)
    path = tmp_path / "invalid_mass.json"
    save_catalog(catalog, str(path))

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        data["items"][0]["mass"] = -10
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)
    with pytest.raises(CorruptedFileError):
        load_catalog(str(path))


def test_load_duplicate_id(tmp_path: Path) -> None:
    catalog = Catalog()
    detail1 = Detail(
        "ART-0042",
        "Шестерня привода",
        "Механика",
        date(2026, 11, 12),
        1.45,
        "Сталь",
    )
    detail2 = Detail(
        "ART-0043",
        "Шестерня привода",
        "Механика",
        date(2026, 11, 12),
        1.45,
        "Сталь",
    )
    catalog.add(detail1)
    catalog.add(detail2)
    path = tmp_path / "duplicate_id.json"
    save_catalog(catalog, str(path))

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        data["items"][1]["identifier"] = "ART-0042"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)
    with pytest.raises(CorruptedFileError):
        load_catalog(str(path))


def test_load_into_catalog_adds_contents(tmp_path: Path) -> None:
    current = Catalog()
    old_detail = Detail(
        "OLD",
        "Старая деталь",
        "Механика",
        date(2026, 11, 10),
        1.0,
        "Сталь",
    )
    current.add(old_detail)

    source = Catalog()
    detail_b = Detail(
        "B",
        "Шестерня",
        "Механика",
        date(2026, 11, 11),
        1.5,
        "Сталь",
    )
    detail_c = Detail(
        "C",
        "Болт",
        "Крепёж",
        date(2026, 11, 12),
        0.1,
        "Медь",
    )
    source.add(detail_b)
    source.add(detail_c)

    path = tmp_path / "additional_details.json"
    save_catalog(source, str(path))

    load_into_catalog(current, str(path))

    assert len(current) == 3
    assert list(current) == [old_detail, detail_b, detail_c]
    assert current.get("OLD") is old_detail


def test_load_empty_file_preserves_contents(tmp_path: Path) -> None:
    current = Catalog()
    old_detail = Detail(
        "OLD",
        "Старая деталь",
        "Механика",
        date(2026, 11, 10),
        1.0,
        "Сталь",
    )
    current.add(old_detail)

    source = Catalog()
    path = tmp_path / "empty.json"
    save_catalog(source, str(path))

    load_into_catalog(current, str(path))

    assert len(current) == 1
    assert list(current) == [old_detail]
    assert current.get("OLD") is old_detail


def test_load_into_catalog_preserves_state_on_error(tmp_path: Path) -> None:
    current = Catalog()
    old_detail = Detail(
        "OLD",
        "Старая деталь",
        "Механика",
        date(2026, 11, 10),
        1.0,
        "Сталь",
    )
    current.add(old_detail)
    original_data = asdict(old_detail)

    source = Catalog()
    detail_b = Detail(
        "B",
        "Шестерня",
        "Механика",
        date(2026, 11, 11),
        1.5,
        "Сталь",
    )
    detail_c = Detail(
        "C",
        "Болт",
        "Крепёж",
        date(2026, 11, 12),
        0.1,
        "Медь",
    )
    source.add(detail_b)
    source.add(detail_c)

    path = tmp_path / "invalid_second_record.json"
    save_catalog(source, str(path))

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    data["items"][1]["mass"] = -10

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    with pytest.raises(CorruptedFileError):
        load_into_catalog(current, str(path))

    assert len(current) == 1
    assert list(current) == [old_detail]
    assert current.get("OLD") is old_detail
    assert asdict(current.get("OLD")) == original_data
    assert "B" not in current
    assert "C" not in current


def test_load_into_catalog_preserves_state_on_id_conflict(tmp_path: Path) -> None:
    current = Catalog()
    old_detail = Detail(
        "OLD",
        "Исходная деталь",
        "Механика",
        date(2026, 11, 10),
        1.0,
        "Сталь",
    )
    current.add(old_detail)
    original_data = asdict(old_detail)

    source = Catalog()
    detail_b = Detail(
        "B",
        "Шестерня",
        "Механика",
        date(2026, 11, 11),
        1.5,
        "Сталь",
    )
    conflicting_detail = Detail(
        "OLD",
        "Другая деталь",
        "Гидравлика",
        date(2026, 11, 12),
        2.0,
        "Медь",
    )
    source.add(detail_b)
    source.add(conflicting_detail)

    path = tmp_path / "id_conflict.json"
    save_catalog(source, str(path))

    with pytest.raises(DuplicateIdError):
        load_into_catalog(current, str(path))

    assert len(current) == 1
    assert list(current) == [old_detail]
    assert current.get("OLD") is old_detail
    assert asdict(old_detail) == original_data
    assert "B" not in current


def test_replace_with_uses_independent_storage() -> None:
    source = Catalog()
    detail = Detail(
        "ART-0042",
        "Шестерня",
        "Механика",
        date(2026, 11, 12),
        1.45,
        "Сталь",
    )
    source.add(detail)

    target = Catalog()
    target.replace_with(source)

    source.remove(detail.identifier)

    assert len(source) == 0
    assert len(target) == 1
    assert target.get(detail.identifier) is detail


def test_load_invalid_utf8(tmp_path: Path) -> None:
    path = tmp_path / "invalid_utf8.json"
    path.write_bytes(b"\xff")

    with pytest.raises(CorruptedFileError):
        load_catalog(str(path))


def test_large_integer_mass_json_round_trip(tmp_path: Path) -> None:
    mass = 10**1000
    detail = Detail(
        "LARGE-0001",
        "Тестовая деталь",
        "Механика",
        date(2026, 11, 12),
        mass,
        "Сталь",
    )
    catalog = Catalog()
    catalog.add(detail)
    path = tmp_path / "large_mass.json"

    save_catalog(catalog, str(path))
    loaded = load_catalog(str(path))
    restored = loaded.get(detail.identifier)

    assert len(loaded) == 1
    assert list(loaded) == [detail]
    assert isinstance(restored.mass, int)
    assert restored.mass == mass
