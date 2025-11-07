from django.contrib import admin

from ..models import FinancialInstitution
from .base import BaseModelAdmin


@admin.register(FinancialInstitution)
class FinancialInstitutionAdmin(BaseModelAdmin[FinancialInstitution]):  # type: ignore[type-arg]
    ...
