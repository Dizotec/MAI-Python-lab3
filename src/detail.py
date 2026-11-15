from dataclasses import dataclass
from datetime import date
from math import isfinite

from src.errors import InvalidDetailError


def check(value,field)-> None:
    if not(isinstance(value,str)):
        raise InvalidDetailError(f"{field} must be a string")
    if not(value.strip()):
        raise InvalidDetailError(f"{field} must be not empty")


    
@dataclass(frozen = True)
class Detail:
    identifier: str 
    name: str 
    category: str 
    date: date 
    mass: float 
    material: str 
    def __post_init__(self) -> None:
        check(self.identifier,"identifier")
        check(self.name,"name")
        check(self.category,"category")
        check(self.material,"material")
        if not(isinstance(self.mass, (int, float))) or isinstance(self.mass,bool) or not(isfinite(self.mass)):
            raise InvalidDetailError("Mass must be finite int or float number")
        if self.mass <= 0:
            raise InvalidDetailError("Mass must be positive number")
        if not(isinstance(self.date,date)):
            raise InvalidDetailError("Incorrect date")

        
        
        
        