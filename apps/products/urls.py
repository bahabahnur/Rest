from django.urls import path, include
from rest_framework import routers
from apps.products.views import (
    OwnerProductsViewSet, CustomerProductsAPIView, WishDelete, WishAdd, WishListApiView
)

router = routers.DefaultRouter()
router.register('owner_products', OwnerProductsViewSet, basename='products')

urlpatterns = [
    path('customer_products/', CustomerProductsAPIView.as_view()),
    path('wishlist/', WishListApiView.as_view()),
    path('<int:pk>/wish/add/', WishAdd.as_view()),
    path('<int:pk>/wish/delete/', WishDelete.as_view()),

]
urlpatterns += router.urls

