from hope_control_manager.models import FinancialInstitution

from .base import AutoRegisterModelFactory


class FinancialInstitutionFactory(AutoRegisterModelFactory):
    class Meta:
        model = FinancialInstitution
