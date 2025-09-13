from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from products.models import Products, Categories
from products.serializers import ProductsSerializer, CategoriesSerializer
from e_commerce_application.pagination import CustomPageNumberPagination
from .filters import ProductFilter


class ProductMixin:
    def _get_paginated_products(self, request, queryset=None, Serilizer=None):
        # Default we will get only the products with is_deleted "False".
        queryset = queryset or Products.objects.all().filter(is_deleted=False)
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(queryset, request)
        serializer = Serilizer(paginated_products, many=True) if Serilizer else ProductsSerializer(paginated_products,
                                                                                                   many=True)
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


class CategoryListView(APIView, ProductMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.query_params.get("name")
        # In case we need to see all the category in the future.
        show_all_category = request.query_params.get("show_all_category")
        if show_all_category:
            categories = Categories.objects.all()
        else:
            categories = Categories.objects.filter(name=name) if name else Categories.objects.filter(is_deleted=False)
        return self._get_paginated_products(request, categories, CategoriesSerializer)

    def post(self, request):
        # Expect a list of category objects: [{"name": "Category1"}, {"name": "Category2"}]
        categories_data = request.data.get("categories")
        if not categories_data or not isinstance(categories_data, list):
            return Response({"error": "Expected a list of categories."}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: Avoid duplicates
        existing_names = set(
            Categories.objects.filter(name__in=[categorie.get('name') for categorie in categories_data]).values_list(
                'name', flat=True))
        categories_to_create = [categorie for categorie in categories_data if
                                categorie.get('name') not in existing_names]

        if not categories_to_create:
            return Response({"message": "All categories already exist."}, status=status.HTTP_200_OK)

        serializer = CategoriesSerializer(data=categories_to_create, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data},
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        category_id = request.data.get('category_id')
        if not category_id or not isinstance(category_id, int):
            return Response({"error": "Field 'category_id'(int) is required."}, status=status.HTTP_400_BAD_REQUEST)

        category = Categories.objects.get(id=category_id)
        if category:
            category.is_deleted = True
            category.save()
            return Response({"Success": f"Category ID {category_id} deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)

        return Response({"error": f"Category ID {category_id} not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, format=None):
        category_id = request.data.get('id')
        if not category_id or not isinstance(category_id, int):
            return Response({"error": "Field 'category_id'(int) is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            return Response({"error": f"Category ID{id} not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriesSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
