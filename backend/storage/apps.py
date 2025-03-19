from django.apps import AppConfig
import socket
import requests
from django.db.models.signals import post_migrate
import sys

class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storage'

    def ready(self):
        from django.contrib.sites.models import Site
        from django.db.utils import OperationalError, ProgrammingError

        def is_migration():
            """Проверяет, выполняются ли сейчас миграции"""
            return "migrate" in sys.argv or "makemigrations" in sys.argv

        def is_local():
            """Определяет, локальный ли запуск."""
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                return local_ip.startswith("127.") or hostname == "localhost"
            except socket.gaierror:
                return True  # В случае ошибки считаем, что локально

        def get_server_ip():
            """Определяет внешний IP сервера, если он не локальный."""
            try:
                response = requests.get("https://api64.ipify.org?format=text", timeout=3)
                return response.text.strip()
            except requests.RequestException:
                return "localhost:8000"

        def update_site(sender, **kwargs):
            """Обновляет домен в базе данных"""
            try:
                if is_migration():
                    domain = "localhost:8000"  # Во время миграции всегда localhost
                elif is_local():
                    domain = "localhost:8000"  # При локальном запуске тоже localhost
                else:
                    domain = get_server_ip()  # В облаке берем реальный IP

                Site.objects.update_or_create(
                    id=1,
                    defaults={"domain": domain, "name": domain}
                )
            except (OperationalError, ProgrammingError):
                pass

        # Привязываем обработчик обновления домена при миграции и запуске сервера
        post_migrate.connect(update_site, sender=self)
