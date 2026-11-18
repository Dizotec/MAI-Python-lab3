import json
from datetime import date

from src.catalog import Catalog
from src.detail import Detail
from src.errors import (
    CorruptedFileError,
    DuplicateIdError,
    InvalidDetailError,
    UnsupportedFormatVersionError,
)


def save_catalog(catalog: Catalog, path: str) -> None:
    result = []
    for detail in catalog:
        record = {}
        record["identifier"] = detail.identifier
        record["name"] = detail.name
        record["date"] = detail.date.isoformat()
        record["mass"] = detail.mass
        record["category"] = detail.category
        record["material"] = detail.material
        result.append(record)

    root_record = {}
    root_record["format_version"] = 1
    root_record["items"] = result
    with open(path, "w", encoding="UTF-8") as file:
        json.dump(root_record, file, ensure_ascii=False, indent=2)


def load_catalog(path: str) -> Catalog:
    with open(path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise CorruptedFileError("Incorrect JSON")
        if not (isinstance(data, dict)):
            raise CorruptedFileError
        if "format_version" not in data:
            raise CorruptedFileError
        if isinstance(data["format_version"], bool):
            raise CorruptedFileError
        if not isinstance(data["format_version"], int):
            raise CorruptedFileError
        if data["format_version"] != 1:
            raise UnsupportedFormatVersionError
        if "items" not in data:
            raise CorruptedFileError
        if not (isinstance(data["items"], list)):
            raise CorruptedFileError
        catalog = Catalog()
        for record in data["items"]:
            if not isinstance(record, dict):
                raise CorruptedFileError
            if "identifier" not in record:
                raise CorruptedFileError
            if "name" not in record:
                raise CorruptedFileError
            if "date" not in record:
                raise CorruptedFileError
            if "mass" not in record:
                raise CorruptedFileError
            if "category" not in record:
                raise CorruptedFileError
            if "material" not in record:
                raise CorruptedFileError
            try:
                detail = Detail(
                    identifier=record["identifier"],
                    name=record["name"],
                    date=date.fromisoformat(record["date"]),
                    mass=record["mass"],
                    category=record["category"],
                    material=record["material"],
                )
                catalog.add(detail)
            except (
                ValueError,
                TypeError,
                InvalidDetailError,
                DuplicateIdError,
            ) as error:
                raise CorruptedFileError("Invalid entry") from error
        return catalog


def load_into_catalog(catalog: Catalog, path: str) -> None:
    loaded = load_catalog(path)
    combined = Catalog()
    for detail in catalog:
        combined.add(detail)
    for detail in loaded:
        combined.add(detail)
    catalog.replace_with(combined)
