import os

from django.db import models


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.title}{ext}'
    return f'product/{final_name}'


class ShopSetting(models.Model):
    title = models.CharField('نام شرکت', max_length=100)
    adress = models.CharField('آدرس', max_length=500)
    telephone = models.CharField('تلفن', max_length=20)
    mobile = models.CharField('موبایل', max_length=20)
    email = models.EmailField('ایمیل')
    aboutus = models.TextField('درباره ما', null=True, blank=True)
    image = models.ImageField('تصویر', null=True, blank=True,default='default.jpg')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.title