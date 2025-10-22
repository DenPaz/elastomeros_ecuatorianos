from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoreConfig(AppConfig):
    name = "apps.store"
    verbose_name = _("Store")

    def ready(self):
        import apps.users.signals  # noqa: F401, PLC0415
