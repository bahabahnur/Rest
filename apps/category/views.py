from rest_framework.generics import(
    ListAPIView,
)
from apps.category.serializers import CategoryAPISerializer
from apps.category.models import Category


class CategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAPISerializer
