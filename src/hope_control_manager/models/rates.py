from django.db import models

from hope_control_manager.models.base import AbstractModel


class ExchangeRate(AbstractModel):
    name = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.name
