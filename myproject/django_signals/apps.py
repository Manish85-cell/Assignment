from django.apps import AppConfig


class DjangoSignalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_signals'

    def ready(self):
        import django_signals.signals
