# Generated by Django 3.2.25 on 2024-04-27 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopproducts', '0004_productgallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopproducts.product', verbose_name='محصول'),
        ),
    ]