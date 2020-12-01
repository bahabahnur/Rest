from django.urls import path

from . import views

urlpatterns = [
    path('create-order/', views.OrderCreateAPIView.as_view()),
    path('order/<int:pk>/', views.OrderDetailAPIView.as_view()),
    path('my_orders/', views.OrderAuthorListAPIView.as_view()),
]
