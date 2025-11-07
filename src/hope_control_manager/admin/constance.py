from constance.admin import Config, ConstanceAdmin
from django.contrib import admin

from .base import BaseModelAdmin

admin.site.unregister([Config])


@admin.register(Config)
class ConstanceConfigAdmin(ConstanceAdmin[Config], BaseModelAdmin):  # type: ignore[misc]
    pass
