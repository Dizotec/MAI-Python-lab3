from src.errors import InvalidDetailError, ItemNotFoundError , DuplicateIdError
from src.catalog import Catalog 
from src.detail import Detail
from datetime import date 
import pytest 
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
    detail = Detail("ART-0042","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    with pytest.raises(ItemNotFoundError):
        catalog.remove("ART-0067")  
def test_duplicate_catalogs_check()->None:
    catalog1 = Catalog()
    catalog2 = Catalog()
    detail = Detail("ART-0042","Шестерня привода 1","Механика",date(2026,11,12),1.45,"Сталь")
    catalog1.add(detail)
    assert len(catalog1) ==1 
    assert len(catalog2) == 0 
   
    
