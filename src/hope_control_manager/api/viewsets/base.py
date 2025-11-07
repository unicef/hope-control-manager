from typing import TypeVar

from django.db import models
from rest_framework import permissions, renderers, viewsets
from rest_framework.serializers import BaseSerializer

_MT_co = TypeVar("_MT_co", bound=models.Model, covariant=True)


class BaseConfigViewSet(viewsets.GenericViewSet[models.Model]):
    permission_classes = [permissions.DjangoObjectPermissions]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    serializer_class_list: type[BaseSerializer[models.Model]] = None
    serializer_class_detail: type[BaseSerializer[models.Model]] = None

    def get_serializer_class(self) -> type[BaseSerializer[models.Model]]:
        if self.action == "list" and self.serializer_class_list:
            return self.serializer_class_list
        if self.action == "retrieve" and self.serializer_class_detail:
            return self.serializer_class_detail
        return self.serializer_class  # type: ignore[return-value]


class BaseReadOnlyModelViewSet(BaseConfigViewSet, viewsets.ReadOnlyModelViewSet[models.Model]):
    pass


class BaseViewSet(BaseConfigViewSet, viewsets.ModelViewSet[models.Model]):
    pass
