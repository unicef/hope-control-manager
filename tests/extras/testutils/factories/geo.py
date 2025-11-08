import factory

from hope_control_manager.models import Area, AreaType, Country

from .base import AutoRegisterModelFactory


class CountryFactory(AutoRegisterModelFactory):
    iso_code2 = factory.Sequence(lambda n: n)
    iso_code3 = factory.Sequence(lambda n: n)
    iso_num = factory.Sequence(lambda n: n)

    class Meta:
        model = Country


class AreaTypeFactory(AutoRegisterModelFactory):
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = AreaType


class AreaFactory(AutoRegisterModelFactory):
    geonameid = factory.Sequence(lambda n: n)
    area_type = factory.SubFactory(AreaTypeFactory)
    parent = None

    class Meta:
        model = Area
