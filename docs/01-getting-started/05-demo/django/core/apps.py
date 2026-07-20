from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # Runs once when the app registry is populated — the closest
        # Django has to a startup hook. (There is no shutdown equivalent.)
        from core import pool

        if pool.pool is None:
            pool.pool = pool.FakePool()
