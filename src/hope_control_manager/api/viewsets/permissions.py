from django.contrib.auth.models import Permission

from ..serializers import PermissionSerializer
from .base import BaseReadOnlyModelViewSet


class PermissionViewSet(BaseReadOnlyModelViewSet):
    queryset = Permission.objects.all().order_by("name")
    serializer_class = PermissionSerializer
