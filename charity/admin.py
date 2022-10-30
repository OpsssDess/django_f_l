from django.contrib import admin

from charity.models import *

class ThingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_thing', 'category')

class OfficeAdmin(admin.ModelAdmin):
    list_display = ('address', 'capacity', 'ocupied')
    list_display_links = ('address', 'ocupied', 'capacity')
    search_fields = ('address', 'ocupied', 'capacity')

admin.site.register(Thing, ThingAdmin)
admin.site.register(Office, OfficeAdmin)