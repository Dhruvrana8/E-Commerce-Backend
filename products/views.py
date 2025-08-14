from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Products
from products.serializers import ProductsSerializer
from e_commerce_application.pagination import CustomPageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
class ProductListView(APIView):
    # Only the Admin will be able to use this API
    permission_classes = [IsAuthenticated, IsAdminUser]

    def _get_paginated_products(self, request, product_id=None):
        queryset = Products.objects.filter(id=product_id, is_deleted=False) if product_id else Products.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = ProductsSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get(self, request, format=None):
        product_id = request.query_params.get("id")
        return self._get_paginated_products(request, product_id)

    def post(self, request, format=None):
        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of products."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return self._get_paginated_products(request)  # return updated product list
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            count, _ = Products.objects.update(is_deleted=False)
            return Response({"Success": f"All {count} products deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)