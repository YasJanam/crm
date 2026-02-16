from django.apps import AppConfig


class SaleConfig(AppConfig):
    name = 'sale'

    def ready(self):
        import sale.signals