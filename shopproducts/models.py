from django.contrib.auth.models import User
from django.db import models
import os
from shop_products_category.models import ProductCategory
from django.db.models import Q


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.id}-{instance.title}{ext}'
    return f'product/{final_name}'


class ProductManager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_by_id(self, pk):
        qs = self.get_queryset().filter(id=pk)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def search_products(self, query):
        lookup = (Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(tag__title__icontains=query) |
                  Q(tag__slug__icontains=query))
        return self.get_queryset().filter(lookup, active=True).distinct()

    def get_product_by_category(self, pk):
        return self.get_queryset().filter(category__name__iexact=pk, active=True)


class Product(models.Model):
    title = models.CharField('عنوان', max_length=50)
    description = models.TextField('توضیحات')
    price = models.IntegerField('قیمت')
    image = models.ImageField('تصویر', default='default.jpg')
    active = models.BooleanField('فعال / غیر فعال', default=True)
    category = models.ManyToManyField(ProductCategory, verbose_name='دسته بندی', blank=True)
    visit_count = models.IntegerField('تعداد مشاهده', default=0)

    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/productdetail/{self.id}'


class ProductGallery(models.Model):
    title = models.CharField('عنوان', max_length=50)
    image = models.ImageField('تصویر', null=True, blank=True, default='default.jpg')
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'گالری تصاویر'
        verbose_name_plural = 'گالری تصاویر'

    def __str__(self):
        return self.title


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.TextField('متن نظر')
    created = models.DateTimeField(auto_now_add=True)
