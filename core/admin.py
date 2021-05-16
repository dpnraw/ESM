from django.contrib import admin

from .models import GeoCodingSettings


@admin.register(GeoCodingSettings)
class GeoCodingSettingsAdmin(admin.ModelAdmin):
    '''Admin View for GeoCodingSettings'''

    list_display = (
        'customer_location',
        'sale_location',
        '_last_updated',
    )

    list_display_links = ('_last_updated', )

    list_editable = (
        'customer_location',
        'sale_location',
    )

    def _last_updated(self, obj):
        return obj.modified

    _last_updated.short_description = 'Last Modified'
