from django.db import models


class FinancialInstitution(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.name
