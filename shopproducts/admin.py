from django.contrib import admin
from .models import Product, ProductGallery, Comment


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price')

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(Comment)