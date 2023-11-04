from __future__ import annotations
from datetime import datetime, timedelta

import ExchangeApi
from FreakingCurrency import FreakingCurrency
import json


class CacheCurrency:
    refresh_period: timedelta
    update_time: datetime
    curencies: dict[str, FreakingCurrency] = {}

    def __init__(self, api: ExchangeApi.Exchange, refresh_period: timedelta = timedelta(minutes=5)):
        self.api = api
        self.refresh_period = refresh_period
        self.update_time = datetime.min

    @staticmethod
    def make(json_value: dict) -> CacheCurrency:
        currency: CacheCurrency = CacheCurrency()
        currency.parse(json_value)
        return currency

    def parse(self, json_value: dict):
        data_time_str: str = json_value["meta"]['last_updated_at']
        date_time: datetime = datetime.fromisoformat(data_time_str)
        self.update_time = date_time
        self.curencies = {}
        for key in json_value['data'].keys():
            single_value = json_value['data'][key]
            self.curencies[single_value['code']] = FreakingCurrency.make(single_value['code'], single_value['value'])

    def get_currencies_test(self) -> dict[str, FreakingCurrency]:
        next_update_period = self.update_time + self.refresh_period
        if datetime.now() > next_update_period:
            json_file = open('LatestResponse.json', 'r')
            value: dict = json.loads(json_file.read())
            json_file.close()
            self.parse(value)
            self.update_time = datetime.now()
        return self.curencies

    def get_currencies(self) -> dict[str, FreakingCurrency]:
        next_update_period = self.update_time + self.refresh_period
        if datetime.now() > next_update_period:
            value: dict = self.api.latest()
            self.parse(value)
            self.update_time = datetime.now()
        return self.curencies
