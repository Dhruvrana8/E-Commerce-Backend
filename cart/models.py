from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from products.models import Products


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.cart_items.aggregate(Sum('total_price'))['total_price__sum']

    def __str__(self):
        return f"Cart for {self.user.username}"


# CartItem Model to handle products in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"

    class Meta:
        unique_together = ('cart', 'product')
