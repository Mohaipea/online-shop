from django.contrib import admin
from shop_products_category.models import ProductCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name']


admin.site.register(ProductCategory, CategoryAdmin)
