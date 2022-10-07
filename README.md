

<h1 align>Тестовый проект по работе с Google Таблицами</h1>

Данный скрипт выполняет получение данных из <a href="https://docs.google.com/spreadsheets/d/1UWhlxh0LuIifDrWV6DLffQ9jT-vzCahxAHwPsk6VJJ0/edit#gid=0" target="_blank">гуггл таблицы</a> и их перенос в БД (postresql)

Для работы данного скрипта требуется установленный python v > 3.0, а также установленный postgresql, для удобство просомтра содержимого можно использовать PgAdmin

Чтобы запустить скрипт, скачайте его к себе, далее создайте новое виртуальное окружение:

**Linux/MACoS**: python3 -m venv venv_name
**Windows**: python -m venv venv_name

Далее активируйте его, перейдя в папку  

**Linux/MACoS**: cd /**папка окружения**/bin
**Windows**: cd /**папка окружения**/Source

и далее: activate, для деактивации используйте команду "deactivate"

После этого перейдите в корневую папку проекта и установите все необходимые библиотеки командой:

**Linux/MACoS**: python3 -m pip install -r requirements.txt
**Windows**: python -m pip install -r requirements.txt

После этого из той же папки выполните команду run.py

Скрипт будет забирать данные из гугл таблицы и при изменении их перезаписывать.

Все основные настройки и параметры определены в файле settings.py


