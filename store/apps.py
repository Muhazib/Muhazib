from django.apps import AppConfig

class storeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        import store.views.signal  # noqa
class StoreConfig(AppConfig):
    name = 'store'
