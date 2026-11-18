from dataclasses import dataclass
from datetime import date
from math import isfinite

from src.errors import InvalidDetailError


def check(value, field) -> None:
    if not (isinstance(value, str)):
        raise InvalidDetailError(f"{field} must be a string")
    if not (value.strip()):
        raise InvalidDetailError(f"{field} must be not empty")


@dataclass(frozen=True)
class Detail:
    identifier: str
    name: str
    category: str
    date: date
    mass: float
    material: str

    def __post_init__(self) -> None:
        check(self.identifier, "identifier")
        check(self.name, "name")
        check(self.category, "category")
        check(self.material, "material")
        if isinstance(self.mass, bool) or not isinstance(self.mass, (int, float)):
            raise InvalidDetailError("Mass must be int or float, excluding bool")

        if isinstance(self.mass, float) and not isfinite(self.mass):
            raise InvalidDetailError("Mass must be finite")

        if self.mass <= 0:
            raise InvalidDetailError("Mass must be positive")
        if not (type(self.date) == date):
            raise InvalidDetailError("Incorrect date")
