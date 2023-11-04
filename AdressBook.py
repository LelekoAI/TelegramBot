from CacheCurrency import CacheCurrency
from FreakingCurrency import FreakingCurrency


class AdressBook:

    # метод который группирует валюты по первой букве и подсчитывает количество валют
    @staticmethod
    def get_group_count(currency: CacheCurrency) -> dict[str, int]:
        char_count: dict[str, int] = {}
        for key in currency.curencies.keys():
            first_char: str = key[0]
            if first_char not in char_count.keys():
                char_count[first_char] = 0
            char_count[first_char] += 1
        return char_count

    # метод который группирует первые буквы валют по кличеству выдачи
    @staticmethod
    def create_group_coins(currency: CacheCurrency, max_count: int = 20) -> list[list[str]]:
        char_count: dict[str, int] = AdressBook.get_group_count(currency)
        char_list: list[str] = []
        end_list: list[list[str]] = []
        count: int = 0
        for key in char_count.keys():
            if count + char_count[key] >= max_count and len(char_list) > 0:
                end_list.append(char_list)
                count = char_count[key]
                char_list = [key]
            else:
                char_list.append(key)
                count += char_count[key]
        if len(char_list) > 0:
            end_list.append(char_list)
        return end_list

    # приходит список букв а возвращает список валют
    @staticmethod
    def get_currency_by_group(group: list[str], currency: CacheCurrency) -> dict[str, FreakingCurrency]:
        values: dict[str, FreakingCurrency] = {}
        for key in currency.curencies.keys():
            first_char: str = key[0]
            if first_char in group:
                values[key] = currency.curencies[key]
        return values
