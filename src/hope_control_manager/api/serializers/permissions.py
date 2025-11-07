from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.HyperlinkedModelSerializer[Permission]):
    class Meta:
        model = Permission
        fields = ["url", "name", "codename"]
