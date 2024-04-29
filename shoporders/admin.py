from django.contrib import admin
from shoporders.models import OrderDetails, Order


class orderDetailsAdmin(admin.ModelAdmin):
    list_display = ['owner']


admin.site.register(Order, orderDetailsAdmin)
admin.site.register(OrderDetails)