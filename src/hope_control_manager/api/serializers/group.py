from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer[Group]):
    members = serializers.HyperlinkedIdentityField(
        view_name="group-members-list",
        lookup_url_kwarg="parent_lookup_groups",
    )

    class Meta:
        model = Group
        fields = ["url", "name", "members"]
