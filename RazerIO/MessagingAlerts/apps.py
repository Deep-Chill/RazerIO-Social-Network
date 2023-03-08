from django.apps import AppConfig

class MessagingalertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MessagingAlerts'

    def ready(self):
        import MessagingAlerts.signals