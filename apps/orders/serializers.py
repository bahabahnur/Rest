from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.models import ProductsModel


class OrderCreateForm(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['first_name', 'email', 'address']


class OrderDetailRetrieveSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = ProductsModel
        fields = (
            'id',
            'title',
            'price',
        )

    def get_size(self, obj):
        return obj.get_size_display()
