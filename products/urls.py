from django.urls import path

from products.views import ProductListView, ProductSearchView, CategoryListView, ProductWishListView, \
    remove_product_from_wishlist

urlpatterns=[
    path('', ProductListView.as_view(), name='product-list'),
    path('search/',ProductSearchView.as_view(), name='product-search'),
    path('categories/',CategoryListView.as_view(), name='categories'),
    path('wishlist/', ProductWishListView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>/', remove_product_from_wishlist, name='remove_from_wishlist'),
]