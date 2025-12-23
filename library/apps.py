from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def create_superuser(sender, **kwargs):
    """
    Создаём суперюзера ПОСЛЕ migrate.
    Работает на Render без shell.
    """
    # Только если включил флаг и это прод
    if settings.DEBUG:
        return
    if not getattr(settings, "AUTO_CREATE_SUPERUSER", False):
        return

    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        username = getattr(settings, "AUTO_SUPERUSER_USERNAME", "admin")
        password = getattr(settings, "AUTO_SUPERUSER_PASSWORD", "admin12345")
        email = getattr(settings, "AUTO_SUPERUSER_EMAIL", "admin@example.com")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            print(f"SUPERUSER CREATED: {username} / {password}")
        else:
            print(f"SUPERUSER EXISTS: {username}")
    except Exception as e:
        print("Superuser creation error:", e)


class LibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library"

    def ready(self):
        post_migrate.connect(create_superuser, sender=self)
