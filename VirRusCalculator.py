from FreakingCurrency import FreakingCurrency
from decimal import Decimal


class Claculator:
    @staticmethod
    def calculate(amount: Decimal, against: FreakingCurrency, to: FreakingCurrency):
        return amount*(to.value / against.value)