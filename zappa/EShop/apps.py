from corsheaders.signals import check_request_enabled
from django.apps import AppConfig


class EshopConfig(AppConfig):
    name = 'EShop'

    @staticmethod
    def allow_api(sender, request, **kwargs):
        return True

    def ready(self):
        check_request_enabled.connect(self.allow_api)
