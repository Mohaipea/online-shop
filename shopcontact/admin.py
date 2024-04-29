from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'seen', 'subject']
    list_filter = ['seen']
    list_editable = ['seen', 'subject']
    search_fields = ['subject', 'name']


admin.site.register(Contact, ContactAdmin)

