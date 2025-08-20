from django.urls import path

from products.views import ProductListView, ProductSearchView


urlpatterns=[
    path('', ProductListView.as_view(), name='product-list'),
    path('search/',ProductSearchView.as_view(), name='product-search'),
]