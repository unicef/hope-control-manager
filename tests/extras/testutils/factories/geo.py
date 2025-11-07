import factory

from hope_control_manager.models import Area, AreaType, Country

from .base import AutoRegisterModelFactory


class CountryFactory(AutoRegisterModelFactory):
    class Meta:
        model = Country


class AreaTypeFactory(AutoRegisterModelFactory):
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = AreaType


class AreaFactory(AutoRegisterModelFactory):
    area_type = factory.SubFactory(AreaTypeFactory)
    parent = None

    class Meta:
        model = Area
