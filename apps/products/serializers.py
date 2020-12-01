from rest_framework import serializers
from apps.category.serializers import CategoryAPISerializer
from apps.products.models import ProductsModel, Wish


class ProductsAPISerializer(serializers.ModelSerializer):
    # category = CategoryAPISerializer(many=False)

    class Meta:
        model = ProductsModel
        fields = ('id', 'title', 'image',  'description', 'price', 'author', 'category')


class WishAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('product', 'user')
