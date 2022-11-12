from django.contrib import admin
from django.utils.safestring import mark_safe

from charity.models import *


class DonationInline(admin.StackedInline):
    model = DonationItem
    extra = 1

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_thing', 'category')
    list_display_links = ('id', 'name', 'type_thing',)
    search_fields = ('name', 'type_thing', 'category')
    readonly_fields = ('category',)
    list_filter = ('category', 'type_thing')
    inlines = [DonationInline]


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('address', 'capacity', 'ocupied')
    list_display_links = ('address', 'ocupied', 'capacity')
    search_fields = ('address', 'ocupied', 'capacity')

admin.site.register(Office, OfficeAdmin)


@admin.register(DonationItem)
class DonationItemAdmin(admin.ModelAdmin):
    list_display = ('donation', 'base_item_hash', 'office')
    list_display_links = ('donation', 'base_item_hash', 'office')
    search_fields = ('base_item_hash', 'office')


@admin.register(RequestItem)
class RequestItemAdmin(admin.ModelAdmin):
    list_display = ('request', 'base_item_hash', 'office')
    list_display_links = ('request', 'base_item_hash', 'office')
    search_fields = ('base_item_hash', 'office')


@admin.register(ItemDescription)
class ItemDescriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'details', 'condition', 'base_item_hash', 'office', 'get_html_image')
    list_display_links = ('name', 'details', 'condition',)
    search_fields = ('base_item_hash', 'office')

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")