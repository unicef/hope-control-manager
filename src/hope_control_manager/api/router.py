from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import viewsets as vs


class RootView(APIRootView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class ApiRouter(ExtendedDefaultRouter):
    APIRootView = RootView


router = ApiRouter()
(
    router.register("users", vs.UserViewSet, basename="user")
    .register("groups", vs.GroupViewSet, basename="user-groups", parents_query_lookups=["user_groups"])
    .register(
        "permissions", vs.PermissionViewSet, basename="user-permissions", parents_query_lookups=["group__user", "group"]
    )
)
(
    router.register("groups", vs.GroupViewSet, basename="group").register(
        "members", vs.UserViewSet, basename="group-members", parents_query_lookups=["groups"]
    )
)
(router.register("permissions", vs.PermissionViewSet, basename="permission"))
