<<<<<<< HEAD
import django_filters 
=======
from django_filters import rest_framework
import django_filters
>>>>>>> 3a172affb8f288737825eee3a250fcb31de1f400
from reviews import models


class TitleFilter(django_filters.FilterSet):
<<<<<<< HEAD
    name = django_filters.CharFilter(lookup_expr='contains', field_name='name')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='in')
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='in')

    class Meta:
        model = models.Title
        fields = ('name', 'category__slug', 'genre__slug', 'year')
=======
    genre = rest_framework.CharFilter(field_name='genre__slug')
    name = rest_framework.CharFilter(lookup_expr='contains', field_name='name')
    category = rest_framework.CharFilter(field_name='category__slug')

    class Meta:
        model = models.Title
        fields = ['genre__slug', 'name', 'category__slug', 'year']
        
>>>>>>> 3a172affb8f288737825eee3a250fcb31de1f400
