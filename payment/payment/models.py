from django.db import models


# Create your models here.
class Item(models.Model):
    """Товар"""
    name = models.CharField('Название', max_length=30)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Discount(models.Model):
    """Скидки"""
    user_id = models.IntegerField('id пользователя', default=1)
    discount = models.DecimalField('Скидка', decimal_places=2, max_digits=5)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    """Налоги"""
    user_id = models.IntegerField('id пользователя', default=1)
    tax = models.DecimalField('Налог', decimal_places=2, max_digits=5)

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Orders(models.Model):
    """Заказы"""
    user_id = models.IntegerField('id пользователя', default=1)
    items = models.ManyToManyField(Item, verbose_name='Товары')
    discount = models.ForeignKey(Discount, verbose_name='Скидка', on_delete=models.PROTECT, null=True)
    tax = models.ForeignKey(Tax, verbose_name='Налог', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
