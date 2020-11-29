from rest_framework import serializers
from apps.category.serializers import CategoryAPISerializer
from apps.products.models import ProductsModel


class ProductsAPISerializer(serializers.ModelSerializer):
    category = CategoryAPISerializer(many=False)

    class Meta:
        model = ProductsModel
        fields = 'title', 'image',  'description', 'price', 'author', 'category'
