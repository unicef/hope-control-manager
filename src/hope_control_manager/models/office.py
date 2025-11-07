from typing import Any

from django.db import models


class BusinessArea(models.Model):
    code = models.CharField(max_length=10, unique=True)
    slug = models.CharField(max_length=250, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.parent:
            self.parent.is_split = True
            self.parent.save()
        if self.children.count():  # type: ignore[attr-defined]
            self.is_split = True
        super().save(*args, **kwargs)
