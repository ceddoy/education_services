## **Обучающий мини-сервис для тестирования по заданным темам**
В данном сервисе вы можете создать различные обучающие темы в админ-панели (Django Admin), добавлять теоретические описания к ним. К каждой теме вы можете добавить любое количество вопросов с вариантами ответов (правильных ответов можно создать несколько). При переходе на интересующую Вас тему, и после ознакомления с теоретической частью вам будет предложено пройти тестирование (если будет хотя бы 1 вопрос создан), вопросы будут идти последовательно, после каждого ответа, вам будет предоставлен комментарий о правильности ответа, после прохождения теста вы будете уведомлены о своих результатах, а также результат будет продублирован на электронную почту. В админ-панели в разделе о пользователях будет размещена вся история прохождения тестов пользователем, а также в админ-панели вы можете редактировать/добавлять/удалять темы, вопросы и ответы.
### Реализованы следующие задачи:
**Адмика Django:**
* Создание обучающей темы и описание к нему;
* Создание/редактирование/удаление вопроса к теме с несколькими вариантами ответов (вопросы валидируются на внесение минимум одного правильного ответа);
* Просмотр в разделе пользователей историю прохождения тестов по различным темам;

**API:**

* Регистрация пользователя по email;
* Стандартная авторизация юзера по токену;
* Просмотр списка обучающих тем;
* Просмотр отдельно обучающих тем с теоретическим описанием и с дальнейшей возможностью пройти тест по данной теме;
* Просмотр и выбор ответа/ответов на каждый вопрос теста;


### Инструменты разработки:

**Стек:**

* Django 4.0.3
* DRF 3.13.1
* PostgreSQL 14
* celery 4.3.0
* redis 4.1.4


**Обращаю ваше внимание на переменные в settings.py, необходимо присвоить им значения**


Для запуска сервиса вам необходимо установить **docker, docker-compose*, после сделать следующее: 
Введите в терминале корня проекта команду:
```
* docker-compose up --build
```
Ждем, когда все зависимости и сервисы установятся и запустятся.

Готово! Пользуйтесь.
На забудьте создать админа:
```
python manage.py createsuperuser
```
### API points:
в качестве тестирования прошу использовать приложение postman, либо сайт https://www.postman.com/, можно также использоват спецификацию **/swagger/**

**1) Регистрация пользователей  -**
**/api/clients/create/**
#### Поля для заполнения (POST-запрос) - Body -> raw -> JSON
```
{
    "email": "mail01@mail.ru",
    "password": "123454321qw"
}
```

**2) Авторизация пользователя -**
**/api-token-auth/**
#### Поля для заполнения (POST-запрос) - Body -> raw -> JSON
```
{
    "email": "mail01@mail.ru",
    "password": "123454321qw"
}
```
**получаем Token для дальнейшего прохождения по проекту.**

**3) Просмотр списка обучающих тем -**
**/api/topics/** - (GET-запрос)

JSON ответ:
```
[
    {
        "id": 1,
        "title": "Природа"
    },
    {
        "id": 2,
        "title": "Космос"
    }
]
```

**4) Просмотр обучающей темы -**
/api/topics/<int:pk>/ - (GET-запрос)

В JSON ответе вы получите **start_testing_url** для старта теста:
```
{
    "id": 1,
    "title": "Природа",
    "description": "Природа - это.....",
    "start_testing_url": "/api/test/2/"
}
```

**5) Просмотр вопроса -**
**api/test/<int:pk>/** - (GET-запрос)

**Обязательно перед стартом каждого вопроса необходимо сделать GET-запрос**

JSON ответ:
```
{
    "question_text": "Какой вид топлива самый распространенный и древний?",
    "answers": [
        {
            "id": 1,
            "answer_text": "Уголь"
        },
        {
            "id": 2,
            "answer_text": "Дрова"
        },
        {
            "id": 3,
            "answer_text": "Нефть"
        }
    ]
}
```

**6) Ответ на вопрос -**
**api/test/<int:pk>/**
#### Поля для заполнения (POST-запрос) - Body -> raw -> JSON
***id ответа берем из JSON ответа в GET-запросе вопроса***
```
{
    "id": [2]
}
```
Если варинтов ответа несколько:
```
{
    "id": [2, 3]
}
```
Затем получаем JSON ответ:
Если ответили правильно:
```
{
    "result": "Правильно",
    "next_question": "/api/test/3/"
}
```
Если ответили неправильно:
```
{
    "result": "Неправильно",
    "correct_answer": [
        {
            "id": 2,
            "answer_text": "Дрова"
        }
    ],
    "next_question": "/api/test/3/"
}
```
**next_question** используем для перехода (GET-запрос) на следующий вопрос.

После окончания всех вопросов по заданной теме:
```
{
    "result": "Правильно, тест окончен",
    "result_answers": {
        "correct": 15,
        "wrong": 5
    }
}
```
*Кратная скрин-инструкция, как создать вопрос с ответами:*

![Image alt](https://github.com/ceddoy/education_services/raw/master/images_for_readme/screen_admin-panel.jpg)
