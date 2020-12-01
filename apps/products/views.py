from datetime import timedelta

from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, generics, serializers
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import ProductsModel, Wish
from apps.products.permissions import IsOwner
from apps.products.serializers import ProductsAPISerializer, WishAPISerializer


class CustomerProductsAPIView(ListAPIView):
    """даем разрешение на заказы"""
    queryset = ProductsModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsAPISerializer
    page_size = 1


class MyPaginationClass(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            description = data[i]['description']
            if len(description) > 5:
                data[i]['description'] = description[:5] + 'ещё'
        return super().get_paginated_response(data=data)


class OwnerProductsViewSet(viewsets.ModelViewSet):
    """даем разрешение владельцу редакатировать"""
    serializer_class = ProductsAPISerializer
    queryset = ProductsModel.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_queryset(self):
        return ProductsModel.objects.filter(
            author=self.request.user
        )

    @action(detail=False, methods=['get'])   # /new?t=hour
    def new(self, request, pk=None):
        t = request.query_params.get('t')
        queryset = self.get_queryset()
        if t:
            if t == 'hour':
                start_time = timezone.now() - timedelta(hours=1)
            elif t == 'week':
                start_time = timezone.now() - timedelta(weeks=1)
            elif t == 'minutes':
                start_time = timezone.now() - timedelta(minutes=1)
        else:
            start_time = timezone.now() - timedelta(days=1)
        queryset = queryset.filter(created_at__gte=start_time)
        serializer = ProductsAPISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        print(queryset)
        serializer = ProductsAPISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishListApiView(generics.ListCreateAPIView):
    serializer_class = WishAPISerializer

    def get_queryset(self):
        queryset = Wish.objects.all()
        return Wish.objects.filter(user=self.request.user.id)

    def post(self, request, *args, **kwargs):
        if len(request.data.keys()) == 1 and request.data.get('продукт'):
            user = request.user.id
            product = request.data['product']
            favorites = Wish.objects.filter(product=product, user=user.id)
            if favorites:
                raise serializers.ValidationError('Товар в уже в избранных')
            request.data['user'] = request.user.id

        else:
            raise serializers.ValidationError('Извините у вас ошибка')
            pass
        return self.create(request, *args, **kwargs)


class WishAdd(APIView):

    def get(self, request, pk):
        product = ProductsModel.objects.get(pk=pk)
        user = request.user
        url = request.build_absolute_uri()
        if Wish.objects.filter(user=user.id, product=pk):
            raise serializers.ValidationError('ОК')
        new_favorite = Wish.objects.create(user=user, product=product)
        return HttpResponseRedirect(redirect_to=url)


class WishDelete(APIView):

    def get(self, request, pk):
        user = request.user
        print(user)
        product = ProductsModel.objects.get(pk=pk)

        favor = Wish.objects.filter(user=user.id, product=pk)
        print(favor)
        if favor:
            favor.delete()
            raise serializers.ValidationError('Удалили1')
        raise serializers.ValidationError('Нету')
