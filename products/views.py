from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from products.models import Products
from products.serializers import ProductsSerializer
from e_commerce_application.pagination import CustomPageNumberPagination
from .filters import ProductFilter


class ProductMixin:
    def _get_paginated_products(self, request, queryset=None):
        # Default we will get only the products with is_deleted "False".
        queryset = queryset or Products.objects.all().filter(is_deleted=False)
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(queryset, request)
        serializer = ProductsSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)


# Create your views here.
class ProductListView(APIView, ProductMixin):
    # Only the Admin will be able to use this API
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):
        product_id = request.query_params.get("id")
        products = Products.objects.all().filter(id=product_id) if product_id else None
        return self._get_paginated_products(request, products)

    def post(self, request, format=None):
        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of products."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return self._get_paginated_products(request)  # return updated product list

        error_response = []
        for index, errors_for_item in enumerate(serializer.errors):
            original_data = request.data[index]
            product_name = original_data.get('name')

            if errors_for_item:
                error_response.append({
                    "product_name": product_name,
                    "errors": errors_for_item
                })

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        product_id = request.data.get('id')

        if product_id:  # Delete a specific product
            try:
                product = Products.objects.get(id=product_id)
                product.is_deleted = True
                product.save()
                return Response({"Success": f"Product ID {product_id} deleted successfully."},
                                status=status.HTTP_204_NO_CONTENT)
            except Products.DoesNotExist:
                return Response({"Error": f"Product ID {product_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        else:  # No ID means delete all products
            Products.objects.update(is_deleted=True)
            return Response({"Success": f"All products deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, format=None):
        product_id = request.data.get("id")
        if not product_id:
            return Response({"error": "Field 'id' is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({"error": f"Product ID {product_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self._get_paginated_products(request, product_id=product_id)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSearchView(APIView, ProductMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Products.objects.filter(is_deleted=False)
        filter = ProductFilter(request.query_params, queryset=queryset)

        filtered_products = filter.qs

        if not filter.is_valid():
            return Response(filter.errors, status=status.HTTP_400_BAD_REQUEST)

        return self._get_paginated_products(request, filtered_products)
