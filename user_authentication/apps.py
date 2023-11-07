from django.apps import AppConfig


class UserAuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_authentication"

    def ready(self):
        import user_authentication.signals