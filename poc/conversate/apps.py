from django.apps import AppConfig

class ConversateConfig(AppConfig):
    name = 'conversate'
    verbose_name = 'Conversate Application'
 
    def ready(self):
        import conversate.signals
