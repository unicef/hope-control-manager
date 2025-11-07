from django.contrib import admin

from ..models import Area, AreaType, Country
from .base import BaseModelAdmin


@admin.register(Country)
class CountryAdmin(BaseModelAdmin[Country]):  # type: ignore[type-arg]
    ...


@admin.register(AreaType)
class AreaTypeAdmin(BaseModelAdmin[AreaType]):  # type: ignore[type-arg]
    pass


@admin.register(Area)
class AreaAdmin(BaseModelAdmin[Area]):  # type: ignore[type-arg]
    pass
