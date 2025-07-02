# Module-4.2-v2
API autotests booking


<h1 align="center">Привет! Меня зовут <a href="https://github.com/AldaDyrroth" target="_blank">Алдар</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">Проект посвящен API автотестам публичной API сервиса по имитации бронирования номеров</h3>

Цель проекта - тестирование открытого API-портала, имитирующего работу сервиса онлайн-бронирования. Применены негативное и контрактное тестирования.


## API
https://restful-booker.herokuapp.com/apidoc/index.html


## Объект тестирования
В рамках проекта покрыты следующие методы:

GET `/booking` получить список броней 

GET `/booking/:id` получить информацию по конкретной брони 

POST `/booking` создать бронь 

PUT `/booking/:id` перезаписать бронь

PATCH `/booking/:id` обновить данные брони 

DELETE `/booking/:id` удалить бронь 


## Используемые технологии:
pytest
pydantic


Для запуска проекта введите команду (пока не работает):
```
cd tests/
python test_bookings.py

```

### Описание модулей

`booking_client.py` - API-клиент для отправки запросов со встроенной валидацией данных

`models.py` - хранит модели данных для отправки запросов и обработки ответов

`test_scenarios.py` - сценарии использвания сервиса, применяет методы, реализованные в `booking_client.py`

`validator.py` - универсальный валидатор данных, сравнивает модели данных запроса и ответа с заданной из models.py, проводит проверку на статус-код

`test_booking.py` - набор конечных тестов




<p align="center">
  <img src="https://i.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.webp" alt="Анимированная радуга" width="300">
</p>

## Команда разработки
Тестировщик Ефремов Алдар

Куратор Дима
