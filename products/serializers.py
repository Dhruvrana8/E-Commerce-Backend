from time import timezone

from rest_framework import serializers

from products.models import  Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
       model = Products
       fields = ['id','name', 'price', 'category', 'description', 'is_deleted', 'created_at', 'updated_at','is_wishlist']
       read_only_fields = ['created_at', 'updated_at']
