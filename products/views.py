from django.contrib.admin.templatetags.admin_list import pagination
from django.core import paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Products
from products.serializers import ProductsSerializer
from .pagination import CustomPageNumberPagination


# Create your views here.
class ProductListView(APIView):
    def get(self, request, format=None):
        products = Products.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_todos = paginator.paginate_queryset(products, request)
        serialized_data = ProductsSerializer(paginated_todos, many=True)
        return paginator.get_paginated_response(serialized_data.data)

    def post(self, request, format=None):
        name = request.data.get('name')
        price = request.data.get('price')
        category = request.data.get('category')
        description = request.data.get('description')

        if name and price and description and category:
            serializer = ProductsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(
            {'Error': 'Name, price, description, and category are required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, format=None):
        id = request.data.get('id')
        if id:
            products = Products.objects.filter(id=id)
            if products:
                products.delete()
                return Response( {"Success":f'The {id} is deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Error': f'ID: {id} not found.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"id is a required field."},status=status.HTTP_400_BAD_REQUEST)