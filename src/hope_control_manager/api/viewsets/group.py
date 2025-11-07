from django.contrib.auth.models import Group

from ..serializers import GroupSerializer
from .base import BaseReadOnlyModelViewSet


class GroupViewSet(BaseReadOnlyModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
