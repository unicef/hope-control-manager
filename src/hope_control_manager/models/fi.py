from django.db import models
from django.utils.translation import gettext as _

from .base import AbstractModel
from .geo import Country


class FinancialInstitution(AbstractModel):
    name = models.CharField(max_length=1000)
    vendor_number = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="ERP Vendor number")
    bank_code = models.CharField(
        max_length=4, blank=True, null=True, unique=True, help_text="Bank code as in linked SWIFT Code"
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Branch(AbstractModel):
    """SWIFT code, also known as a Business Identifier Code (BIC).

    It is an 8-11 character code that identifies banks and financial institutions worldwide,
    enabling international money transfers. It is structured with a bank code, country code,
    location code, and an optional branch code.

    - Bank Code (4 letters): A shorthand name for the bank.
    - Country Code (2 letters): A standard ISO country code.
    - Location Code (2 letters or numbers): Identifies the bank's city or location.
    - Branch Code (3 letters or numbers, optional): Specifies a particular branch. "XXX" indicates the head office.

    """

    institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE)
    swift_code = models.CharField(max_length=11, blank=True, null=True, unique=True, help_text="SWIFT/BIC Code. ")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        ordering = ("institution", "swift_code")
        verbose_name_plural = _("Branches")
