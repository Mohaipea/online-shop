from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from shopproducts.models import Product


class Tag(models.Model):
    title = models.CharField('عنوان', max_length=150)
    slug = models.SlugField('عنوان url', unique=True, blank=True)
    created = models.DateTimeField('زمان ثبت', auto_now_add=True)
    active = models.BooleanField('فعال / غیر فعال', default=True)
    products = models.ManyToManyField(Product, blank=True, verbose_name='محصولات')

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)


