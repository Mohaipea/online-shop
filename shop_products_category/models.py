from django.db import models


class ProductCategory(models.Model):
    title = models.CharField('عنوان', max_length=100)
    name = models.CharField('عنوان url', max_length=100)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title