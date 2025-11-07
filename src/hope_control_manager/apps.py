from django.apps import AppConfig


class Config(AppConfig):
    name = "hope_control_manager"

    def ready(self) -> None:
        from . import checks  # noqa
        from . import handlers  # noqa
        from .utils import flags  # noqa
