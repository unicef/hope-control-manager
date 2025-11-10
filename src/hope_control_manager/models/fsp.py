from django.db import models

from .base import AbstractModel


class FinancialServiceProvider(AbstractModel):
    name = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.name
