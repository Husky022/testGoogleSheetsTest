import requests
import json


# класс менеджер по выгрузке текущего курса валюты с сайта ЦБ
class ExchangeManager:
    def __init__(self, api, valute):
        self.api = api
        self.valute = valute

    # получаем по API значение нужной нам валюты
    def load_exchange(self):
        return json.loads(requests.get(self.api).text)['Valute'][self.valute]['Value']

