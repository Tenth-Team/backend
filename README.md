# MVP CRM-системы для Амбассадоров Яндекс Практикума.

## Описание проекта:

Это CRM система с базой данных, набором функций и селекторами. Система позволяет взаимодействовать с амбассадорами, автоматизировать процессы, анализировать данные.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Tenth-Team/backend.git
```

```
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```


```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Из корневой директории запустить сборку контейнеров с помощью
docker-compose:
```python
docker-compose up -d
```

Документация будет доступка по ссылке http://127.0.0.1/api/swagger/

Для попадания в админ-зону, перейдите по адресу http://127.0.0.1:8000/admin/.


## Стек

* Python 3.10.6
* Django 4.2
* Django REST framework 
* Docker
* Postgres
* Celery 

## Авторы

- [Антон Земцов](https://github.com/antonata-c)
- [Вадим Гуржий](https://github.com/VadimGurzhy)
- [Михаил Зеленчук](https://github.com/qwertttyyy)
- [Шериф Рагимов](https://github.com/ragimov700)
