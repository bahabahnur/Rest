from django.db import models
from apps.category.models import Category
from django.contrib.auth import get_user_model
from django.conf import settings

CURRENCY = settings.CURRENCY

User = get_user_model()


class ProductsModel(models.Model):

    author = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class Wish(models.Model):
    """ Избраннные """
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} --> {self.user}'
