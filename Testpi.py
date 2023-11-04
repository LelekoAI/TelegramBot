import urllib.parse
import json
import os
import datetime
from datetime import datetime
from FreakingCurrency import FreakingCurrency
from VirRusCalculator import Claculator
from CacheCurrency import CacheCurrency
import AdressBook

url1: str = 'https://www.google.com/v3/'
print(urllib.parse.urljoin(url1, './hnya'))
print(urllib.parse.urljoin(url1, None))
url2 = "http://127.0.0.1/test1/test2/test3/test5.xml"
url3 = "../../test4/test6.xml"

print(urllib.parse.urljoin(url2,url3))
exit()

x = json.loads('{"a": []}')
print(type(x))
print(x['a'])

json_file = open('LatestResponse.json', 'r')
value: dict = json.loads(json_file.read())
json_file.close()
data_time_str: str = value["meta"]['last_updated_at']
print(data_time_str)
date_time: datetime = datetime.fromisoformat(data_time_str)
print(date_time)
currencis: dict[str, FreakingCurrency] = {}
for key in value['data'].keys():
    single_value = value['data'][key]
    currencis[single_value['code']] = FreakingCurrency.make(single_value['code'], single_value['value'])

print(currencis)

print(Claculator.calculate(100, currencis['USD'], currencis['RUB']))

currency: CacheCurrency = CacheCurrency.make(value)
pass

char_count: dict[str, int] = {}
for key in currencis.keys():
    first_char: str = key[0]
    if first_char not in char_count.keys():
        char_count[first_char] = 0
    char_count[first_char] += 1
print(char_count)
print(len(currencis))

print(AdressBook.AdressBook.get_group_count(currency))

vir_rus: list[list[str]] = AdressBook.AdressBook.create_group_coins(currency)
print(vir_rus)

vir_rus: list[list[str]] = AdressBook.AdressBook.create_group_coins(currency, 30)
print(vir_rus)

print(AdressBook.AdressBook.get_currency_by_group(vir_rus[2], currency))
