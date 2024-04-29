from django.contrib.auth.models import User
from django.db import models

from shopproducts.models import Product


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    payment_date = models.DateTimeField('تاریخ پرداخت', null=True, blank=True)
    is_paid = models.BooleanField('پرداخت شده / نشده', default=False)
    ref_id = models.CharField('شماره پیگیری تراکنش', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

    def __str__(self):
        return self.owner.username

    def get_total_price(self):
        amount = 0
        for i in self.orderdetails_set.all():
            amount += i.quantity * i.price
        return amount


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سبد خرید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.IntegerField('تعداد')
    price = models.IntegerField('قیمت')

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

    def __str__(self):
        return self.product.title

    def get_detail_sum(self):
        return self.price * self.quantity