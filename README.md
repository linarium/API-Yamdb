# Проект «YaMDb»

## Описание:
Проект YaMDb собирает отзывы пользователей на произведения, которые, в свою очередь, делятся на категории: «Книги», «Фильмы», «Музыка» и тд.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Применяемые технологии / пакеты:
Принципы REST API.
Формат передачи данных - JSON.
Framework - Django, Django REST Framework.
JWT - Simple JWT.
DataBase - SQLite3.
Пакет datetime.
Модуль Requests.
Наполнение базы тестовыми данными из CSV файлов.
Передача данных осуществляется по протоколу HTTP.  
Аутентификация осуществляется по JWT-токену.
#### Документация к API доступна по адресу `http://127.0.0.1:8000/redoc/`

### Процесс регистрации новых пользователей:
1. Пользователь отправляет запрос с параметрами *email* и *username* на **/api/v1/auth/signup/**.  
2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный email-адрес.
3. Пользователь отправляет запрос с параметрами *username* и *confirmation_code* на эндпоинт **/api/v1/auth/token/**, в ответе на запрос ему приходит *token* (JWT-токен).
После регистрации и получения токена пользователь может отправить PATCH-запрос на **/users/me/** и заполнить поля в своём профайле (описание полей — в документации). 



## Процесс установки:

 Клонируем репозиторий и переходим в него через терминал:

 ```$ git clone https://github.com/alklim912/api_yamdb.git```
 ```$ cd api_yamdb```

 Создаем и активируем виртуальное окружение:
 
 ```$ python3 -m venv venv```
 ```$ source venv/bin/activate```
 
 Устанавливаем зависимости из файла requirements.txt:

 ```$ python3 -m pip install --upgrade pip```
 ```$ pip install -r requirements.txt```

 Выполняем миграции:

 ```$ python3 manage.py migrate```

 Запускаем django сервер:

 ```$ python3 manage.py runserver```
 

### Процесс заполнения БД из CSV-файлов:

Выполняется на чистую базу.

Выполняем миграции:

 ```$ python3 manage.py migrate```

Загружаем подготовленные данные:

 ```$ python3 csvinbd.py```


## Пример использования API:

**GET /titles/** - получить список всех произведений  

Удачное выполнение запроса (200):
Ключ|Значение|Описание
----|--------|--------
"id"|integer|ID произведения
"name"|"string"|Название
"year"|integer|Год выпуска
"rating"|integer|Рейтинг на основе отзывов
"description"|"string"|Описание
"genre"|Array of objects|Жанр
||"name"|Название жанра (string)
||"slug"|"slug" (string)
"category"|object|Категория
||"name"|Название категории (string)
||"slug"|"slug" (string)

### Команда разработчиков: [Александр Климентьев](https://github.com/alklim912), [Лина Морган](https://github.com/linarium), [Макс Ракшин](https://github.com/MaxUMEO)