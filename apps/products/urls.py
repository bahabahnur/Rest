from django.urls import path, include
from rest_framework import routers
from apps.products.views import (
    OwnerProductsViewSet, CustomerProductsAPIView
)

router = routers.DefaultRouter()
router.register('owner_products', OwnerProductsViewSet, basename='products')

urlpatterns = [
    path('customer_products/', CustomerProductsAPIView.as_view()),
]
urlpatterns += router.urls

