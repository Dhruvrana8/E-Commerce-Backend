from django.urls import path

from products.views import ProductListView, ProductSearchView, CategoryListView


urlpatterns=[
    path('', ProductListView.as_view(), name='product-list'),
    path('search/',ProductSearchView.as_view(), name='product-search'),
    path('categories/',CategoryListView.as_view(), name='categories'),
]