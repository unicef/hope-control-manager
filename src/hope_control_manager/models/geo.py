# - Country
# - AreaType
# - Area
from typing import Any

from django.db import models
from django.db.models import JSONField, Q, UniqueConstraint
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


class UpgradeModel(models.Model):
    original_id = models.UUIDField(blank=True, null=True)

    class Meta:
        abstract = True


class Country(NaturalKeyModel, MPTTModel, models.Model):
    name = models.CharField(max_length=255, db_index=True, db_collation="und-ci-det")
    short_name = models.CharField(max_length=255, db_index=True, db_collation="und-ci-det")
    iso_code2 = models.CharField(max_length=2, unique=True)
    iso_code3 = models.CharField(max_length=3, unique=True)
    iso_num = models.CharField(max_length=4, unique=True)
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

    def __str__(self) -> str:
        return self.name


class Area(NaturalKeyModel, MPTTModel, UpgradeModel, models.Model):
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
        constraints = [
            UniqueConstraint(
                fields=["p_code"],
                name="unique_area_p_code_not_blank",
                condition=~Q(p_code=""),
            )
        ]
        permissions = (("import_areas", "Can import areas"),)

    class MPTTMeta:
        order_insertion_by = ("name", "p_code")

    def __str__(self) -> str:
        return self.name
