from admin_extra_buttons.decorators import button
from adminfilters.autocomplete import LinkedAutoCompleteFilter
from django.contrib import admin
from django.http import HttpRequest, HttpResponse

from ..models import Area, AreaType, Country
from .base import BaseModelAdmin


@admin.register(Country)
class CountryAdmin(BaseModelAdmin[Country]):  # type: ignore[type-arg]
    list_display = ("short_name", "iso_code2", "iso_code3", "iso_num")
    search_fields = ("name", "short_name")

    @button()  # type: ignore[arg-type]
    def load(self, request: HttpRequest) -> HttpResponse:
        Country.objects.load()
        return None  # type: ignore[return-value]


@admin.register(AreaType)
class AreaTypeAdmin(BaseModelAdmin[AreaType]):  # type: ignore[type-arg]
    list_display = ("name", "country", "level")
    list_filter = (("country", LinkedAutoCompleteFilter.factory(parent=None)), "area_level")
    search_fields = ("name",)


@admin.register(Area)
class AreaAdmin(BaseModelAdmin[Area]):  # type: ignore[type-arg]
    list_display = ("name", "area_type", "p_code", "parent", "area_type__country")
    search_fields = ("name",)
    list_filter = (
        ("area_type__country", LinkedAutoCompleteFilter.factory(parent=None)),
        ("area_type", LinkedAutoCompleteFilter.factory(parent="area_type__country")),
    )
