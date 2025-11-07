from django.contrib import admin

from ..models import FinancialServiceProvider
from .base import BaseModelAdmin


@admin.register(FinancialServiceProvider)
class FinancialServiceProviderAdmin(BaseModelAdmin[FinancialServiceProvider]):  # type: ignore[type-arg]
    ...
