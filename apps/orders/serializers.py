from rest_framework import serializers
from apps.orders.models import Order


class OrderCreateForm(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['first_name', 'email', 'address']
