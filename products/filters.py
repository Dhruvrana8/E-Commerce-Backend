import django_filters
from .models import Products  # Assuming your Products model is here


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.BaseInFilter(field_name='category', lookup_expr='in')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    is_wishlist = django_filters.BooleanFilter(field_name='is_wishlist', lookup_expr='in')

    class Meta:
        model = Products
        fields = ['name', 'category', 'max_price', 'min_price', 'is_wishlist']
