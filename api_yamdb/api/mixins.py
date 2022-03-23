from rest_framework.mixins import (
    CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet


class CreateMixin(GenericViewSet, CreateModelMixin):
    pass


class GetOneMixin(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    pass
