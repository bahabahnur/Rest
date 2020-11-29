from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductsModel
from apps.products.permissions import IsOwner
from apps.products.serializers import ProductsAPISerializer


class CustomerProductsAPIView(ListAPIView):
    """даем разрешение на заказы"""
    queryset = ProductsModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsAPISerializer


class OwnerProductsViewSet(viewsets.ModelViewSet):
    """даем разрешение владельцу редакатировать"""
    serializer_class = ProductsAPISerializer
    queryset = ProductsModel.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_queryset(self):
        return ProductsModel.objects.filter(
            author=self.request.user
        )


