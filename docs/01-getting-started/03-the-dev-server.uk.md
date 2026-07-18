# Сервер для розробки

FastAPI не запускає сам себе. Застосунок FastAPI — це ASGI-*застосунок*
(об'єкт), і щось має насправді відкрити сокет, говорити HTTP і передавати
запити до нього. Це «щось» — ASGI-**сервер**, майже завжди
[Uvicorn](https://www.uvicorn.org/). Цей розділ про те, як запускати ваш
застосунок під час розробки.

## `fastapi dev` — спосіб «з батарейками»

Якщо ви встановили `fastapi[standard]`, у вас є CLI `fastapi`. `fastapi
dev` — це команда для розробки:

```bash
fastapi dev main.py
```

Вона знаходить екземпляр `FastAPI` у `main.py`, запускає Uvicorn з
**увімкненим автоперезавантаженням**, прив'язується до `127.0.0.1:8000` і
друкує, де застосунок та інтерактивна документація:

```
Serving at: http://127.0.0.1:8000
API docs:   http://127.0.0.1:8000/docs
```

Відредагуйте файл, збережіть — і сервер перезапуститься автоматично.

## `uvicorn` — команда під капотом

`fastapi dev` — це зручна обгортка. Під нею — просто Uvicorn, і ви можете
викликати Uvicorn напряму; саме це більшість проєктів кладуть у свої
скрипти:

```bash
uvicorn main:app --reload
```

`main:app` — це `module:variable`, тобто об'єкт `app` у `main.py`. Корисні
прапорці:

```bash
uvicorn main:app --reload                       # dev: auto-reload on
uvicorn main:app --host 0.0.0.0 --port 9000     # bind all interfaces, port 9000
uvicorn main:app --reload --reload-dir app      # only watch ./app for changes
uvicorn main:app --log-level debug              # noisier logs
```

Значення за замовчуванням, які варто знати: host `127.0.0.1`, port `8000`,
reload **вимкнено** (тому `--reload` тут вказано явно, тоді як `fastapi
dev` вмикає його за вас).

> **З досвіду Django:** `uvicorn main:app --reload` — прямий відповідник
> `python manage.py runserver`: локальний HTTP-сервер зі спостерігачем за
> файлами, що перезапускається при збереженні. `manage.py runserver` теж
> за замовчуванням слухає `127.0.0.1:8000` і приймає адресу так, як ви й
> очікуєте: `runserver 0.0.0.0:9000`. Автоперезавантаження там теж
> увімкнено за замовчуванням; `--noreload` вимикає його (відповідник
> чистого `uvicorn` без `--reload`).

## Запуск «по-справжньому»: `fastapi run` і воркери

Ось частина, яка дивує Django-розробників. `manage.py runserver` — це
сервер **тільки для розробки**; документація Django жирним шрифтом
застерігає ніколи не використовувати його в продакшені. З Uvicorn інакше:
він *і є* продакшн-ASGI-сервером. Команди для розробки та для продакшену —
це просто різні профілі однієї програми.

```bash
fastapi run main.py                 # prod profile: no reload, binds 0.0.0.0
fastapi run main.py --workers 4     # 4 worker processes

# the Uvicorn equivalent:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

`--workers N` запускає N незалежних робочих процесів, щоб задіяти кілька
ядер CPU. (Автоперезавантаження та кілька воркерів не поєднуються — reload
працює в одному процесі.)

> **З досвіду Django:** У світі Django сервер для розробки та
> продакшн-сервер — це дві різні програми: ви розробляєте з `runserver`, а
> розгортаєте за Gunicorn чи uWSGI (WSGI) або Uvicorn/Daphne (ASGI). З
> FastAPI немає одноразового dev-сервера, який лишається позаду — ви
> запускаєте Uvicorn в обох місцях, вимикаючи `--reload` і піднімаючи
> `--workers` для продакшену. Масштабування на кілька процесів, яке Django
> віддає Gunicorn (`gunicorn --workers 4`), тут — це `uvicorn --workers 4`.
> Розгортання отримає окремий розділ згодом; зараз ідея в тому, що сервер —
> той самий.

## Кілька слів про перезавантажувач

Автоперезавантажувач стежить за вашими вихідними файлами й перезапускає
процес сервера при зміні. Це **розробницька** можливість в обох
фреймворках — вимикайте її в продакшені (вона додає накладні витрати й
потік спостереження за файлами). `fastapi run` і `uvicorn --workers` уже
залишають її вимкненою; з `runserver` ви б передали `--noreload`.

Одне, що `runserver` робить, а Uvicorn — ні: автоматично роздає ваші
статичні файли в режимі `DEBUG`. FastAPI не має обробки статичних файлів,
доки ви її не додасте — це розглянуто в розділі *Шаблони та статичні
файли*.

## Супровідні проєкти { #companion-projects }

Мінімальний застосунок, побудований обома способами, у каталозі
`03-demo/` цього розділу:

- `03-demo/fastapi/` ([завантажити](03-demo-fastapi.zip)) — запуск через
  `fastapi dev main.py`; тестування через `pytest`.
- `03-demo/django/` ([завантажити](03-demo-django.zip)) — запуск через
  `python manage.py runserver`; тестування через `python manage.py test`.

Щоб вони були чесними щодо *обслуговування запитів*, кожен набір тестів
містить один тест, який піднімає **справжній** сервер по HTTP — Uvicorn у
підпроцесі на боці FastAPI, `manage.py runserver` у підпроцесі на боці
Django — і робить реальний HTTP-запит, а не лише використовує вбудований
тестовий клієнт.

## Джерела

- [FastAPI — Run a server manually (Uvicorn)](https://fastapi.tiangolo.com/deployment/manually/)
- [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/)
- [Uvicorn — settings and command line](https://www.uvicorn.org/settings/)
- [Django — runserver](https://docs.djangoproject.com/en/6.0/ref/django-admin/#runserver)
- [Django — Deploying (why not runserver)](https://docs.djangoproject.com/en/6.0/howto/deployment/)
