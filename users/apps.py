from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from simple_history import register
        from django.contrib.auth.models import Permission

        # Group заменён на CustomGroup, и он proxy — его НЕ надо регистрировать!
        register(Permission)
