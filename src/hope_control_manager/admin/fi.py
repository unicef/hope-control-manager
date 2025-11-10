from adminfilters.autocomplete import AutoCompleteFilter, LinkedAutoCompleteFilter
from adminfilters.value import ValueFilter
from django.contrib import admin

from ..models import Branch, FinancialInstitution
from .base import BaseModelAdmin


@admin.register(FinancialInstitution)
class FinancialInstitutionAdmin(BaseModelAdmin[FinancialInstitution]):  # type: ignore[type-arg]
    list_display = ("name", "vendor_number", "bank_code")
    search_fields = ("name", "bank_code")


@admin.register(Branch)
class BranchAdmin(BaseModelAdmin[FinancialInstitution]):  # type: ignore[type-arg]
    list_display = ("institution", "swift_code", "country")
    search_fields = ("institution__name", "swift_code")
    list_filter = (
        ("institution", LinkedAutoCompleteFilter.factory(parent=None)),
        ("swift_code", ValueFilter),
        ("country", AutoCompleteFilter),
    )
