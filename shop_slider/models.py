import os
from django.db import models


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.id}-{instance.title}{ext}'
    return f'slider/{final_name}'


class Slider(models.Model):
    title = models.CharField('عنوان', max_length=150)
    description = models.TextField('توضیحات')
    link = models.URLField('آدرس', max_length=200)
    image = models.ImageField('تصویر', upload_to=upload_image_path, null=True, blank=True, default='default.jpg')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title