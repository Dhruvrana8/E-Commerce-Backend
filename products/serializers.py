from time import timezone

from rest_framework import serializers

from products.models import  Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
       model = Products
       fields = '__all__'