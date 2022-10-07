import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import settings


# класс - менеджер по работе с Google таблицами
class GoogleSheets:
    def __init__(self, credentials, spreedsheet_id):
        self.credentials = credentials
        self.spreedsheet_id = spreedsheet_id

    # Авторизация и получение доступа к экземпляру таблицы
    def authorize(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        return apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Выгрузка данных, диапазон задан статично
    def unload(self):
        service = self.authorize()
        values = service.spreadsheets().values().get(
            spreadsheetId=self.spreedsheet_id,
            range='A1:D100',  # заданный диапазон
            majorDimension='ROWS'
        ).execute()
        values_output = []
        for item in values['values'][1:]:
            if settings.IGNORE_INCORRECT_ROW and '' in item:  # проверка, если есть пустые ячейки в строке
                continue
            else:
                values_output.append(tuple(item))
        return tuple(values_output)

