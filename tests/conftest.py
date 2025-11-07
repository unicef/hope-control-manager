import os
import sys
import time
from pathlib import Path

from faker import Faker

faker = Faker()


def pytest_addoption(parser):
    pass


def pytest_configure(config):
    here = Path(__file__).parent
    root = here.parent
    sys.path.insert(0, str(here / "extras"))
    sys.path.insert(0, str(root / "src"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hope_control_manager.config.settings")

    from django.conf import settings

    settings.CACHE_PREFIX = str(time.time())
    settings.CSRF_COOKIE_SECURE = False
