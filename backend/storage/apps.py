# from django.apps import AppConfig


# class StorageConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'storage'

#     def ready(self):
#         import storage.signals

from django.apps import AppConfig
import environ

env = environ.Env()

class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storage'

    def ready(self):
        # Импортируем модель Site здесь, чтобы избежать проблем с импортами
        from django.contrib.sites.models import Site

        # Обновляем или создаем сайт при каждом запуске
        Site.objects.update_or_create(
            id=1,
            defaults={
                "domain": env("DOMAIN", default="localhost:8000"),
                "name": env("SITE_NAME", default="localhost"),
            },
        )