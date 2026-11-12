from datetime import date 
from src.detail import Detail
from src.errors import InvalidDetailError
from math import inf 
import pytest
def test_detail_creation() -> None:
    detail = Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
    assert detail.identifier == "ART-0042"
    assert detail.name == "Шестерня привода"
    assert detail.category == "Механика"
    assert detail.date == date(2026,11,12)
    assert detail.mass == 1.45 
    assert detail.material == "Сталь"
def test_detail_empty_identifier()->None:
    with pytest.raises(InvalidDetailError):
        Detail(" ","Шестерня привода","Механика",date(2026,11,12),1.45,"Сталь")
def test_detail_empty_name()->None:
    with pytest.raises(InvalidDetailError):
        Detail("ART-0042"," ","Механика",date(2026,11,12),1.45,"Сталь")
def test_detail_empty_category()->None:
    with pytest.raises(InvalidDetailError):
        Detail("ART-0042","Шестерня привода"," ",date(2026,11,12),1.45,"Сталь")
def test_detail_empty_material()->None:
    with pytest.raises(InvalidDetailError):
        Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),1.45," ")

@pytest.mark.parametrize("mass", [0, -1.5,"1.45",None,False,True,float('nan'),float(inf),float(-inf)])
def test_detail_invalid_mass(mass)->None:
    with pytest.raises(InvalidDetailError):
        Detail("ART-0042","Шестерня привода","Механика",date(2026,11,12),mass,"Сталь")
@pytest.mark.parametrize("date", ["11.12.2026",None])
def test_invalid_data(date)->None:
    with pytest.raises(InvalidDetailError):
        Detail("ART-0042","Шестерня привода","Механика",date,1.45,"Сталь")

    


