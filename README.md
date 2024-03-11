
# MVP CRM-системы для Амбассадоров Яндекс Практикума.

## О проекте

Проект команды №10 в хакатоне Яндекс-Практикума.

## Команда разработчиков

- [Рагимов Шериф](https://github.com/ragimov700)
- [Зеленчук Михаил](https://github.com/qwertttyyy)
- [Земцов Антон](https://github.com/antonata-c)
- [Гуржий Вадим](https://github.com/VadimGurzhy)

## Технологии
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoRESTFramework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Nginx](https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://www.nginx.org)
![CI/CD](https://img.shields.io/badge/CI%2FCD-2088FF?style=for-the-badge&logo=GitHub-Actions&logoColor=white)


## Начало работы

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере для разработки и тестирования.

<details>
<summary><strong>Запуск с использованием Docker</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлены Docker и Docker Compose. Это можно сделать, следуя официальной документации Docker: https://docs.docker.com/get-docker/ и https://docs.docker.com/compose/install/

### Установка и запуск

1. Клонируйте репозиторий на локальный компьютер:
   ```
   git clone git@github.com:Tenth-Team/backend.git
   cd backend/infra
   ```

2. Запустите контейнеры с помощью Docker Compose:
   ```
   docker-compose up --build
   ```

   Теперь приложение должно быть доступно по адресу:

   http://localhost:8000
   
   А документация доступна по адресу:
   
   http://localhost:8000/api/v1/swagger/

</details>

<details>
<summary><strong>Локальный запуск через pip</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлен Python и pip. Рекомендуется использовать виртуальное окружение для изоляции зависимостей проекта.

### Установка и запуск

1. Клонируйте репозиторий на локальный компьютер:
   ```
   git clone git@github.com:Tenth-Team/backend.git
   cd backend/backend
   ```

2. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Запустите проект (пример для Django):
   ```
   python manage.py migrate
   python manage.py runserver
   ```

   Теперь приложение должно быть доступно по адресу:

   http://localhost:8000
   
   А документация доступна по адресу:
   
   http://localhost:8000/api/v1/swagger/
   

</details>

### Ссылка на скриншот документации:

[![Static Badge](https://img.shields.io/badge/Документация_Swagger-Google_Drive-blue?style=for-the-badge)](https://drive.google.com/file/d/1ySTNXQUQZt4djonFki1h1biCSBdJHsIO/view)

