from hope_control_manager.models import FinancialServiceProvider

from .base import AutoRegisterModelFactory


class FinancialServiceProviderFactory(AutoRegisterModelFactory):
    class Meta:
        model = FinancialServiceProvider
