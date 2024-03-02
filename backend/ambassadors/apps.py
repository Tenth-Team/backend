from django.apps import AppConfig


class AmbassadorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ambassadors'
    verbose_name = 'Управление амбассадорами'

    def ready(self):
        import ambassadors.signals  # noqa
