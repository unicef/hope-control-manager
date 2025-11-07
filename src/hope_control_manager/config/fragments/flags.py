from typing import Any

from ..settings import DEBUG

FLAGS_STATE_LOGGING = DEBUG
FLAGS: dict[str, list[Any]] = {
    "DEVELOP_DEBUG_TOOLBAR": [],
    "SHOW_ADMIN_LINK": [],
    "SHOW_OPEN_ISSUE": [],
}
