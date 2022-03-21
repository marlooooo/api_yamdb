from django_filters import rest_framework
from reviews import models


class TitleFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(lookup_expr='contains', field_name='name')
    category = rest_framework.CharFilter(field_name='category__slug', lookup_expr='in')
    genre = rest_framework.CharFilter(field_name='genre__slug', lookup_expr='in')

    class Meta:
        model = models.Title
        fields = ('name', 'category__slug', 'genre__slug', 'year')
        