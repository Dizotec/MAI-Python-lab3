from datetime import date

import pytest

from src.catalog import Catalog
from src.detail import Detail
from src.errors import DuplicateIdError, ItemNotFoundError


def test_create_catalog()->None:
    catalog = Catalog()
    assert len(catalog) == 0 
    detail = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail)

    assert detail is  catalog.get("ART-0042") 
    assert len(catalog) == 1 
    catalog.remove("ART-0042")
    assert len(catalog) == 0 
def test_invalid_id_getting()->None:
    catalog = Catalog()
    detail = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail)
    catalog.remove("ART-0042")
    with pytest.raises(ItemNotFoundError):
        catalog.get("ART-0042")
def test_duplicate_detail()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0042","Шестерня привода 2","Механика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1) 
    with pytest.raises(DuplicateIdError):
        catalog.add(detail2)
    assert detail1 == catalog.get(detail1.identifier)
    assert len(catalog) == 1 
def test_delete_invalid_ID()->None:
    catalog = Catalog()
    Detail("ART-0042","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    with pytest.raises(ItemNotFoundError):
        catalog.remove("ART-0067")  
def test_duplicate_catalogs_check()->None:
    catalog1 = Catalog()
    catalog2 = Catalog()
    detail = Detail("ART-0042","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    catalog1.add(detail)
    assert len(catalog1) ==1 
    assert len(catalog2) == 0 
def test_iter_catalog()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    first_pass = list(catalog)
    second_pass = list(catalog)
    assert first_pass == [detail1,detail2]
    assert second_pass == first_pass    
def test_find_by_category()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)
    result = catalog.find_by_category("Механика")
    assert result == [detail1,detail2]
def test_find_by_category_missing_element()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)
    result = catalog.find_by_category("Электроника")
    assert result == []
def test_find_by_category_empty_result()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)
    result = catalog.find_by_category("Мех")
    assert result == []


@pytest.mark.parametrize("field", ["Шестер", "ШЕСТЕР","шестер"])
def test_find_by_name(field)->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)
    result = catalog.find_by_name(field)
    assert result == [detail1,detail3]
def test_find_by_name_missing_element()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)
    result = catalog.find_by_name("Подшипник")
    assert result == []
def test_find_by_name_empty_request()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)
    result = catalog.find_by_name("")
    assert result == [detail1,detail2,detail3]
def test_find_by_name_independence()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)

    result = catalog.find_by_name("Шестерня")
    assert result 
    result.clear()
    result = catalog.find_by_name("Шестерня")
    assert result == [detail1,detail3]
    assert list(catalog) == [detail1,detail2,detail3]

def test_find_by_category_independence()->None:
    catalog = Catalog()
    detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    detail2 = Detail("ART-0043","Болт крепёжный","Механика",date(2026,11,12),1.45,"Сталь")
    detail3 = Detail("ART-0044","Шестерня насоса","Гидравлика",date(2026,11,12),1.45,"Сталь")
    catalog.add(detail1)
    catalog.add(detail2)
    catalog.add(detail3)

    result = catalog.find_by_category("Механика")
    assert result 
    result.clear()
    result = catalog.find_by_category("Механика")
    assert list(catalog) == [detail1,detail2,detail3]
    assert result == [detail1,detail2]
def test_contains()->None:
   catalog = Catalog()
   detail1 = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
   catalog.add(detail1)
   assert "ART-0042" in catalog 
   assert "ART-0043" not in catalog 
   catalog.remove("ART-0042")
   assert "ART-0042" not in catalog 
   



    
