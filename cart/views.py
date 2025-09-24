from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from products.models import Products


# This is the API used to add the Products to the cart or to increase the quantity
class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({"Error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if cart exists, otherwise create one
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # If item exists, update the quantity; else create a new item
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response({"Message": "Product added to cart."}, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    # We are getting the item_id from the API
    def put(self, request, item_id):
        quantity = request.data.get('quantity')
        if not quantity:
            return Response({"Error": "Quantity must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(user=request.user)
            product = Products.objects.get(id=item_id)
        except Cart.DoesNotExist:
            return Response({"Error": "Cart or Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.get(cart=cart, product=product)

        if cart_item.quantity != quantity and cart_item.quantity >= 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            return Response({"Error": "The Item can not be less that zero "}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": "Item added to cart."}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        try:
            cart = Cart.objects.get(user=request.user)
            product = Products.objects.get(id=item_id)
        except Cart.DoesNotExist or Products.DoesNotExist:
            return Response({"Error": "Product or Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return Response({"Message": "Item removed from cart."}, status=status.HTTP_200_OK)


# This is the API used to view all the products which are added in the cart
class GetCartItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"Error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.cart_items.all()
        items_data = []
        total_sum = 0

        for item in cart_items:
            items_data.append({
                "product_id": item.product.id,
                "product": item.product.name,
                "price": str(item.total_price),
                "quantity": item.quantity,
                "total_price": str(item.total_price),
            })
            total_sum += item.total_price

        return Response(
            {"cart_items": items_data, "total_sum": total_sum, "cart_id": cart.id, "number_of_items": len(items_data)},
            status=status.HTTP_200_OK)


# This is the API used if the user want to remove any items from the cart
class DeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        product_id = request.data.get('product_id')

        try:
            product = Products.objects.get(id=product_id)
            cart = Cart.objects.get(user=request.user)
        except Products.DoesNotExist or Cart.DoesNotExist:
            return Response({"Error": "Product or Cart not found."}, status=status.HTTP_404_NOT_FOUND)


        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"Message": "Product removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"Error": "Product not found in the cart."}, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"Error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({"Message": "Cart deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
