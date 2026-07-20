# Структура проєкту

FastAPI не диктує розкладку проєкту. Немає `startproject`, немає
`settings.py`, немає поняття «застосунків», які ви реєструєте. Проєкт може
бути одним файлом `main.py` і розростатися в пакет, коли цей файл стає
завеликим. Цей розділ показує, як він росте — і як це зіставляється з
поділом на проєкт/застосунок у Django.

## Єдиний інструмент: `APIRouter`

Щойно одного файлу стає замало, ви розбиваєте маршрути на **роутери**.
`APIRouter` — це міні-колекція операцій шляху, яку ви будуєте в окремому
модулі, а потім приєднуєте до застосунку:

```python
# app/routers/items.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/items", tags=["items"])

ITEMS = [{"id": 1, "name": "Widget"}, {"id": 2, "name": "Gadget"}]


@router.get("")
def list_items():
    return {"items": ITEMS}


@router.get("/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
```

`APIRouter` поводиться як `FastAPI` для оголошення маршрутів — ті самі
декоратори `@router.get(...)` — але сам по собі нічого не обслуговує. Ви
під'єднуєте його до застосунку через `include_router`:

```python
# app/main.py
from fastapi import FastAPI

from app.routers import items, users

app = FastAPI(title="Project Structure (FastAPI)")

app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "It works!"}
```

`prefix="/items"` на роутері означає, що його маршрути живуть під `/items`
(`""` → `/items`, `/{item_id}` → `/items/{item_id}`). `tags=["items"]`
групує їх в UI `/docs`. Це і весь механізм: будуєте роутери в модулях,
`include_router` їх у `main.py`.

> **З досвіду Django:** `include_router(items.router)` — прямий відповідник
> `path("", include("items.urls"))`. `APIRouter` із `prefix` — це, по суті,
> `urls.py` застосунку з приєднаним URL-префіксом. Але це *все*, чим він є —
> група маршрутів. Django-**застосунок** — це набагато більше: набір
> `models.py`, міграцій, `admin.py`, шаблонів і `urls.py`, зареєстрований
> в `INSTALLED_APPS`. Роутер не несе нічого з цього. Тож один
> Django-застосунок зазвичай стає на боці FastAPI *просто* модулем-роутером
> (плюс окремі модулі для моделей/схем/залежностей, які ви додасте згодом).

## Розкладка, що масштабується

Стандартна для спільноти форма застосунку, що росте, — це пакет із
підпакетом `routers/` (або `routers`/`api`):

```
app/
├── __init__.py
├── main.py            # creates FastAPI(), includes the routers
└── routers/
    ├── __init__.py
    ├── items.py       # APIRouter(prefix="/items")
    └── users.py       # APIRouter(prefix="/users")
```

Запускайте це через `fastapi dev app/main.py` (або
`uvicorn app.main:app --reload`). У міру зростання проєкту ви додаєте
сусідні модулі — `models.py`, `schemas.py`, `dependencies.py`,
`database.py`, `config.py` — туди, де, на вашу думку, їм місце. Жодна з цих
назв не нав'язана; це домовленості, а не правила фреймворку.

> **З досвіду Django:** Дві звички, від яких треба відучитися.
>
> По-перше, **немає `INSTALLED_APPS` і немає реєстру застосунків.** Нічого
> не автовиявляється. `main.py` імпортує кожен роутер і явно викликає
> `include_router` — що ви імпортували, те й працює. Немає `apps.py`,
> немає `AppConfig`, немає хука `ready()`, немає фази завантаження
> застосунків.
>
> По-друге, **поділу на проєкт/застосунок не існує.** Django дає вам
> проєкт (`config/`), що володіє налаштуваннями та кореневим URLconf, і
> застосунки, які до нього під'єднуються. У FastAPI є лише «ваш код»:
> екземпляр `FastAPI()` і ті модулі, які ви в нього імпортуєте. `main.py`
> грає суміщену роль підключення `settings.py` і кореневого `urls.py`, але
> ви збираєте це вручну.

## Роутери роблять трохи більше, ніж групують URL

`APIRouter` також може приєднати `prefix`, `tags`, `dependencies` та
типові `responses` до кожного маршруту, який він тримає, а роутери можуть
включати інші роутери — тож ви можете будувати дерево (`/api/v1/items`),
вкладаючи їх:

```python
api = APIRouter(prefix="/api/v1")
api.include_router(items.router)     # -> /api/v1/items
api.include_router(users.router)     # -> /api/v1/users
app.include_router(api)
```

> **З досвіду Django:** Вкладання роутерів для побудови `/api/v1/...` — це
> те, що роблять вкладені виклики `include()` в URLconf Django.
> `dependencies=[...]` на рівні роутера (кожен маршрут у роутері їх
> виконує) — приблизний відповідник обгортання в'ю застосунку в middleware
> чи спільний декоратор, але з областю дії роутера — і це належно
> розглянуто в темі про впровадження залежностей.

## Супровідні проєкти { #companion-projects }

Розкладка вище, побудована обома способами, у каталозі `04-demo/` цього
розділу:

- `04-demo/fastapi/` ([завантажити](04-demo-fastapi.zip)) — пакет `app/` із
  `routers/items.py` та `routers/users.py`, з'єднані в `app/main.py`.
- `04-demo/django/` ([завантажити](04-demo-django.zip)) — проєкт `config/`
  із застосунками `items/` та `users/`, кожен `include()`-нутий у
  `config/urls.py`.

Обидва надають той самий API `/items` та `/users`; їхні тести перевіряють
однакові відповіді. FastAPI: `pytest` (7 тестів). Django: `manage.py test`
(6 тестів, розподілених між двома застосунками).

## Джерела

- [FastAPI — Bigger Applications, multiple files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI — APIRouter reference](https://fastapi.tiangolo.com/reference/apirouter/)
- [Django — URL dispatcher, `include()`](https://docs.djangoproject.com/en/6.0/ref/urls/#include)
- [Django — Applications and the app registry](https://docs.djangoproject.com/en/6.0/ref/applications/)
