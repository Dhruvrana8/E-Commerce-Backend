from django.urls import path

from .views import GetCartItemsView, AddCartItemView, DeleteCartItemView, ClearCartView, UpdateCartItemView

urlpatterns = [
    path('items/', GetCartItemsView.as_view(), name='view-product-cart'),
    path('item/', AddCartItemView.as_view(), name='add-product-cart'),
    path('item/remove/', DeleteCartItemView.as_view(), name='remove-product-cart'),
    path('item/clear/', ClearCartView.as_view(), name='clear-cart'),
    path('item/<int:item_id>/', UpdateCartItemView.as_view(), name='add-cart'),
]
