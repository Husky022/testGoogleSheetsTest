import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import sqlalchemy

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, BigInteger, DATE


# Класс - менеджер по работе с БД
class DBManager:
    def __init__(self, user, password, database_name):
        self.meta = MetaData()
        self.table = None
        self.user = user  # имя пользователя
        self.password = password  # пароль пользователя
        self.database_name = database_name  # имя базы данных
        self.database_table_name = 'Поставки'
        self.check_table('Поставки')

    # Создание таблицы базы данных
    def create_table_in_db(self, db_engine):
        self.table = Table(
            self.database_table_name, self.meta,
            Column('№', Integer, primary_key=True, unique=True),
            Column('заказ №', BigInteger),
            Column('стоимость в руб.', BigInteger),
            Column('срок поставки', DATE),
        )

    # Создание базы данных
    def create_db(self):
        connection = psycopg2.connect(user=self.user, password=self.password)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f'create database {self.database_name}')
        cursor.close()
        connection.close()

    # Подключение к базе данных
    def connect_to_db(self):
        engine = create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@localhost/{self.database_name}",
                               echo=False)
        connection = engine.connect()
        return connection

    # Проверка на существование базы данных
    def check_db(self):
        try:
            connection = self.connect_to_db()
        except sqlalchemy.exc.OperationalError:
            self.create_db()
            connection = self.connect_to_db()
        return connection

    # Проверка на существование таблицы
    def check_table(self, table_name):
        engine = self.check_db()
        meta = MetaData(engine)
        if engine.dialect.has_table(engine, table_name):
            self.table = Table(table_name, meta, autoload=True)
        else:
            self.create_table_in_db(engine)

    # Запись новых данных в базу данных
    def recording(self, values, currency):
        engine = create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@localhost/{self.database_name}",
                               echo=False)
        connection = engine.connect()
        table_delete = self.table.delete()
        connection.execute(table_delete)
        insert = self.table.insert()
        data_list = []
        for item in values:
            data_list.append({'№': item[0],
                              'заказ №': item[1],
                              'стоимость в руб.': int(item[2]) * currency,
                              'срок поставки': item[3]})
        connection.execute(insert, data_list)

    def get_data(self):
        engine = create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@localhost/{self.database_name}",
                               echo=False)
        connection = engine.connect()
        result = connection.execute(self.table.select())
        data_list = []
        for item in result:
            item_to_str = []
            for el in item:
                el_to_str = str(el)
                item_to_str.append(el_to_str)
            # изменение формата даты
            date = item_to_str[-1].split('-')
            date_format = f'{date[2]}.{date[1]}.{date[0]}'
            item_to_str[-1] = date_format
            data_list.append(tuple(item_to_str))
        return tuple(data_list)
