from ..serializers.user import User, UserDetailSerializer, UserListSerializer
from .base import BaseReadOnlyModelViewSet


class UserViewSet(BaseReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class_list = UserListSerializer
    serializer_class_detail = UserDetailSerializer
