from unicef_security.models import AbstractUser, SecurityMixin

from .base import AbstractModel


class User(SecurityMixin, AbstractUser, AbstractModel):  # type: ignore[misc]
    class Meta:
        abstract = False
