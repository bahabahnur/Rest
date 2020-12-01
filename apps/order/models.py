from django.db import models

from apps.products.models import ProductsModel
from apps.authentication.models import User


class Order(models.Model):
    product = models.ManyToManyField(ProductsModel, related_name='products')
    first_name = models.CharField(max_length=50, )
    last_name = models.CharField(max_length=50, )
    address = models.CharField(max_length=250, )
    city = models.CharField(max_length=100, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.value * self.qty
