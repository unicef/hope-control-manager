import factory

from hope_control_manager.models import Branch, FinancialInstitution

from .base import AutoRegisterModelFactory
from .geo import CountryFactory


class FinancialInstitutionFactory(AutoRegisterModelFactory):
    class Meta:
        model = FinancialInstitution


class BranchFactory(AutoRegisterModelFactory):
    institution = factory.SubFactory(FinancialInstitutionFactory)
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = Branch
