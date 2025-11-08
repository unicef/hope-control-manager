# - Country
# - AreaType
# - Area
from typing import Any

import requests
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from mptt.querysets import TreeQuerySet
from natural_keys import NaturalKeyModel


class ValidityQuerySet(TreeQuerySet):
    def active(self, *args: Any, **kwargs: Any) -> "ValidityQuerySet":
        return super().filter(valid_until__isnull=True).filter(*args, **kwargs)


class ValidityManager(TreeManager):
    _queryset_class = ValidityQuerySet

    def load(self) -> None:
        res = requests.get(
            "https://restcountries.com/v3.1/all?fields=name,cca2,cca3,idd,flags,gini,ccn3,subregion", timeout=60
        )
        data = [
            Country(
                short_name=entry["name"]["common"],
                name=entry["name"]["official"],
                iso_code2=entry["cca2"],
                iso_code3=entry["cca3"],
                iso_num=entry["ccn3"],
                lft=0,
                rght=0,
                tree_id=0,
                level=0,
            )
            for entry in res.json()
        ]
        Country.objects.bulk_create(
            data,
            update_conflicts=True,
            unique_fields=["iso_code2"],
            update_fields=["short_name", "name", "iso_code3", "iso_num"],
        )


class Country(NaturalKeyModel, MPTTModel, models.Model):
    name = models.CharField(max_length=255, db_index=True, db_collation="und-ci-det")
    short_name = models.CharField(max_length=255, db_index=True, db_collation="und-ci-det")
    iso_code2 = models.CharField(max_length=2, unique=True, help_text="ISO 3166-1 alpha-2 two-letter country codes")
    iso_code3 = models.CharField(max_length=3, unique=True, help_text="ISO 3166-1 alpha-3 three-letter country codes")
    iso_num = models.CharField(max_length=4, unique=True, help_text="ISO 3166-1 numeric code (UN M49)")

    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent"),
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        on_delete=models.CASCADE,
    )
    valid_from = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    extras = JSONField(default=dict, blank=True)

    objects = ValidityManager()

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_choices(cls) -> list[dict[str, Any]]:
        queryset = cls.objects.all().order_by("name")
        return [
            {
                "label": {"English(EN)": country.name},
                "value": country.iso_code3,
            }
            for country in queryset
        ]


class AreaType(NaturalKeyModel, MPTTModel, models.Model):
    name = models.CharField(max_length=255, db_index=True, db_collation="und-ci-det")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    area_level = models.PositiveIntegerField(default=1)
    parent = TreeForeignKey(
        "self",
        blank=True,
        db_index=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Parent"),
    )
    valid_from = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    extras = JSONField(default=dict, blank=True)

    objects = ValidityManager()

    class Meta:
        verbose_name_plural = "Area Types"
        unique_together = ("country", "area_level", "name")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Area(NaturalKeyModel, MPTTModel, models.Model):
    geonameid = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        "self",
        blank=True,
        db_index=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Parent"),
    )
    p_code = models.CharField(max_length=32, blank=True, null=True, verbose_name="P Code")
    area_type = models.ForeignKey(AreaType, on_delete=models.CASCADE)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    valid_from = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    extras = JSONField(default=dict, blank=True)

    objects = ValidityManager()

    class Meta:
        verbose_name_plural = "Areas"
        ordering = ("name",)
        permissions = (("import_areas", "Can import areas"),)

    class MPTTMeta:
        order_insertion_by = ("name", "p_code")

    def __str__(self) -> str:
        return self.name
