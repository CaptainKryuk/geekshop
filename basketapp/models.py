from django.db import models
from django.conf import settings
from authapp.models import User

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )

    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum([x.quantity for x in _items])
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum([x.product_cost for x in _items])
        return _total_cost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user)

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(id=pk)