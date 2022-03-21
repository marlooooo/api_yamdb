import django_filters 
from reviews import models


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', field_name='name')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='in')
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='in')

    class Meta:
        model = models.Title
        fields = ('name', 'category__slug', 'genre__slug', 'year')
