from django.contrib import admin

from charity.models import *

class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'thing', 'amount', 'time_create', 'stock', 'state', 'office')
    list_display_links = ('id', 'thing')
    search_fields = ('thing', 'office')
    list_editable = ('office', 'state')
    list_filter = ('amount', 'time_create', 'office', 'state')

class OfficeAdmin(admin.ModelAdmin):
    list_display = ('address', 'capacity', 'ocupied')
    list_display_links = ('address', 'ocupied', 'capacity')
    search_fields = ('address', 'ocupied', 'capacity')

admin.site.register(Good, GoodAdmin)
admin.site.register(Office, OfficeAdmin)