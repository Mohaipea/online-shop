# Generated by Django 3.2.25 on 2024-04-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsetting', '0002_shopsetting_aboutus'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopsetting',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='', verbose_name='تصویر'),
        ),
    ]
