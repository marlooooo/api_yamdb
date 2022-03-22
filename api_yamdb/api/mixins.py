from rest_framework.mixins import (
    CreateModelMixin
)
from rest_framework.viewsets import GenericViewSet


class CreateMixin(GenericViewSet, CreateModelMixin):
    pass
