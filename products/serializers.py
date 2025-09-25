from rest_framework import serializers

from products.models import Products, Categories, Wishlist


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
       model = Products
       fields = ['id','name', 'price', 'category', 'description', 'is_deleted', 'created_at', 'updated_at']
       read_only_fields = ['created_at', 'updated_at']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
       model = Categories
       fields = "__all__"
       read_only_fields = ['created_at', 'updated_at']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
        read_only_fields=['created_at']