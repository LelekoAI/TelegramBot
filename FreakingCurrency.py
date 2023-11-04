from __future__ import annotations
from decimal import Decimal


class FreakingCurrency:
    def __init__(self, name: str, value: Decimal):
        self.name: str = name
        self.value: Decimal = value

    @staticmethod
    def make(name: str, value: float) -> FreakingCurrency:
        return FreakingCurrency(name, Decimal(value))

    def __str__(self) -> str:
        return f'{self.name} {self.value}'

    def __repr__(self) -> str:
        return self.__str__()
