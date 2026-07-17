# Встановлення FastAPI та ваш перший застосунок

Цей розділ запускає застосунок FastAPI і будує той самий невеликий API
двома способами — раз на FastAPI, раз на Django — щоб форма різниці була
відчутною від самого початку. Обидві версії постачаються як
[супровідні проєкти](#companion-projects), які можна запустити й
протестувати.

## Встановлення

FastAPI — це звичайний пакет із PyPI. Створіть віртуальне середовище й
встановіть його — додаток `[standard]` підтягує ті частини, які вам
насправді знадобляться в розробці (сервер Uvicorn, CLI `fastapi`, `httpx`
для тестового клієнта, Jinja2 та підтримку форм/файлів):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "fastapi[standard]==0.139.2"
```

Це і все встановлення. Немає жодного `startproject`, жодного `settings.py`,
жодного згенерованого дерева каталогів — ви створюєте порожній файл `.py`
і починаєте писати.

> **З досвіду Django:** `pip install Django`, потім `django-admin
> startproject config .` розкладає пакет проєкту (`settings.py`,
> `urls.py`, `wsgi.py`, `asgi.py`) і `manage.py`. FastAPI не розкладає
> нічого. Плюс — нуль церемоній; мінус — структура, налаштування та точки
> входу стають рішеннями, які ви ухвалюєте самі (у темі 1 є цілий розділ
> про розкладку проєкту).

## Ваш перший застосунок

Помістіть це у `main.py`:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI(title="First App (FastAPI)")

ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
    {"id": 3, "name": "Gizmo"},
]


@app.get("/")
def read_root():
    return {"message": "It works!"}


@app.get("/items")
def list_items(limit: int = 10):
    return {"items": ITEMS[:limit]}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
```

Відбуваються три речі, і всі вони керуються сигнатурами функцій:

- **Маршрутизація — це декоратор.** `@app.get("/items")` прив'язує шлях і
  HTTP-метод безпосередньо до функції. Немає окремої таблиці URL.
- **Поверніть `dict` — отримаєте JSON.** FastAPI серіалізує повернуте
  значення й виставляє `content-type: application/json`. Для типового
  випадку ви взагалі не торкаєтеся об'єкта відповіді.
- **Параметри типізовані й валідовані.** `item_id: int` означає, що
  сегмент шляху розбирається й валідується як ціле число;
  `limit: int = 10` стає необов'язковим параметром запиту зі значенням за
  замовчуванням.

### Запуск

```bash
fastapi dev main.py          # the fastapi[standard] CLI, with auto-reload
# or, equivalently:
uvicorn main:app --reload
```

Відкрийте <http://127.0.0.1:8000/items>, а потім
<http://127.0.0.1:8000/docs> для інтерактивного Swagger UI, який FastAPI
згенерував із тих самих сигнатур.

> **З досвіду Django:** `fastapi dev main.py` — це `manage.py runserver`
> цього світу: dev-сервер з автоперезавантаженням. Різниця під капотом:
> `runserver` — це WSGI dev-сервер, а Uvicorn — ASGI-сервер, і UI `/docs`
> не має відповідника в `runserver` — щоб отримати щось подібне, ви б
> потягнулися до Browsable API з DRF або `drf-spectacular`.

## Той самий API у Django

Ось той самий API, побудований на в'ю Django. Django потребує пакета
проєкту, застосунку, таблиці URL і в'ю, що повертають `JsonResponse`:

```python
# config/urls.py
from django.urls import path
from items import views

urlpatterns = [
    path("", views.read_root),
    path("items", views.list_items),
    path("items/<int:item_id>", views.get_item),
]
```

```python
# items/views.py
from django.http import JsonResponse

ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
    {"id": 3, "name": "Gizmo"},
]


def read_root(request):
    return JsonResponse({"message": "It works!"})


def list_items(request):
    limit = int(request.GET.get("limit", 10))  # convert/validate by hand
    return JsonResponse({"items": ITEMS[:limit]})


def get_item(request, item_id):
    for item in ITEMS:
        if item["id"] == item_id:
            return JsonResponse(item)
    return JsonResponse({"detail": "Item not found"}, status=404)
```

Поставте їх поруч — і розподіл обов'язків стає очевидним:

| | FastAPI | Django |
|---|---|---|
| Прив'язка URL → обробник | декоратор `@app.get("/items")` | запис у `urlpatterns` |
| Читання параметра запиту | `limit: int = 10` (розбір + валідація) | `int(request.GET.get("limit", 10))` (вручну) |
| Повернення JSON | `return {...}` | `return JsonResponse({...})` |
| Сигнал «не знайдено» | `raise HTTPException(404, ...)` | `JsonResponse({...}, status=404)` |
| Інтерактивна документація | вбудована на `/docs` | не вбудована |

## Одна різниця, яку варто помітити вже зараз: погані вхідні дані

Запросіть `/items/abc` — не-ціле число там, де очікується цілий id — і два
фреймворки розходяться:

```http
GET /items/abc

# FastAPI → 422 Unprocessable Entity
#   {"detail":[{"type":"int_parsing","loc":["path","item_id"], ...}]}

# Django  → 404 Not Found
```

FastAPI оголошує `item_id: int`, тож він *валідує* шлях і повертає
структурований `422` з описом того, що було не так. URL-конвертер
`<int:item_id>` у Django просто не збігається з не-цілим числом, тож
резолвер провалюється до `404` — в'ю ніколи не виконується. Той самий
намір (відхилити погані вхідні дані), різний механізм і різний код статусу.
Обидва супровідні проєкти мають тест, що фіксує саме цю поведінку.

> **З досвіду Django:** У DRF ви б отримали помилки валідації у стилі
> FastAPI (`400/422`) від серіалізатора, але чистий Django залишає
> валідацію окремих параметрів на вас — виклик `int()` у `list_items` вище
> підняв би `ValueError` (`500`) на `?limit=abc`. Модель FastAPI «підказка
> типу — це валідація» ближча до DRF, ніж до в'ю Django, але вона вбудована
> в сигнатуру функції, а не в окремий клас серіалізатора.

## Супровідні проєкти { #companion-projects }

Обидва застосунки вище — це повноцінні робочі проєкти в каталозі
`02-demo/` цього розділу:

- `02-demo/fastapi/` — `main.py`, тести, `requirements.txt`. Запуск через
  `fastapi dev main.py`; тестування через `pytest`.
- `02-demo/django/` — проєкт `config/` + застосунок `items/`. Запуск через
  `python manage.py runserver`; тестування через `python manage.py test`.

Кожна сторона має невеликий набір тестів (шість тестів), що перевіряють
показані тут відповіді, включно з різницею `422`/`404`. Кожен розділ,
починаючи звідси, постачається з такою парою.

## Джерела

- [FastAPI — First steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI — Path parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/)
- [Uvicorn — deployment/running](https://www.uvicorn.org/)
- [Django — Writing your first Django app, part 1](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django — URL dispatcher (path converters)](https://docs.djangoproject.com/en/6.0/topics/http/urls/)
- [Django — JsonResponse](https://docs.djangoproject.com/en/6.0/ref/request-response/#jsonresponse-objects)
