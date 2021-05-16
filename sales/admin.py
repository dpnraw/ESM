from datetime import (
    datetime,
    timedelta,
)

from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import mark_safe
from mapbox_location_field.admin import MapAdmin
from rangefilter.filter import DateRangeFilter

from core.models import GeoCodingSettings

from .models import (
    EggType,
    Payment,
    Sale,
    SaleItem,
)
from .queries import QUERY_WHITELIST


@admin.register(EggType)
class EggTypeAdmin(admin.ModelAdmin):
    '''Admin View for EggType'''

    list_display = ('type', )


class SaleItemInline(admin.TabularInline):
    '''Tabular Inline View for SaleItem '''

    model = SaleItem
    min_num = 1
    max_num = 5
    extra = 0


class PaymentInline(admin.TabularInline):
    '''Tabular Inline View for Payment '''

    model = Payment
    min_num = 1
    max_num = 3
    extra = 0


@admin.register(Sale)
class SaleAdmin(MapAdmin, admin.ModelAdmin):
    '''Admin View for Sale'''

    fields = (
        'date',
        'customer',
        'location',
        'signature',
    )

    list_display = (
        'date',
        'customer',
        '_location',
        'descriptive_location',
        'sale_items',
        'total_price',
        'amount_received',
        'due_balance',
        'cheque_balance',
        'salesman',
    )

    list_filter = (
        ('date', DateRangeFilter),
        'date',
        'salesman',
        'descriptive_location',
        'customer',
        'sales__egg_type',
    )

    autocomplete_fields = ('customer', )

    change_list_template = 'admin/sales/sale/change_list.html'

    ordering = (
        '-date',
        'customer',
    )

    date_hierarchy = 'date'

    inlines = (
        SaleItemInline,
        PaymentInline,
    )

    def save_model(self, request, obj, form, change):
        # Add the salesman who perform the sale.
        obj.salesman = request.user
        super(SaleAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Superuser can view all the sales,but salesman can view sales
        # performed by him/her only.
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(salesman=request.user)

    def changelist_view(self, request: HttpRequest, extra_context=None):

        # Superuser can view all the sales,but salesman can view sales
        # performed by him/her only.
        if request.user.is_superuser:
            queryset = Sale.objects.all()
        else:
            queryset = Sale.objects.filter(salesman=request.user)

        # Convert querydict to dict.
        query_parameters = request.GET.dict()
        for filter_tag, value in query_parameters.items():

            # Doesn't break if user mistakenly input wrong query parameters.
            if filter_tag not in QUERY_WHITELIST:
                continue

            # Date range filter tweak for query parameter.
            if 'range__lte' in filter_tag:
                filter_tag = filter_tag.replace('range__lte', 'lt')
                # Adding a day to apply lt filter.
                if value is not None and value != '':
                    x = datetime(*[int(item) for item in value.split('-')])
                    value = (x + timedelta(1)).strftime("%Y-%m-%d")
                else:
                    pass
            if 'range__gte' in filter_tag:
                filter_tag = filter_tag.replace('range__gte', 'gte')
            if value == '':
                continue
            filter_dict = {filter_tag: value}
            # Using a string as the argument to a Django filter query
            queryset = queryset.filter(**filter_dict)

        amount_received = 0.0
        total_price = 0.0
        due_balance = 0.0
        cheque_balance = 0.0

        for record in queryset:
            amount_received += record.amount_received
            total_price += record.total_price
            due_balance += record.due_balance
            cheque_balance += record.cheque_balance

        extra_context = {
            'amount_received': amount_received,
            'total_price': total_price,
            'due_balance': due_balance,
            'cheque_balance': cheque_balance,
        }

        # Call the superclass changelist_view to render the page.
        return super().changelist_view(request, extra_context)

    def total_price(self, obj):
        '''Return total payable price for the individual sale.

        Args:
            obj (Sale): Sale object

        Returns:
            float: Total payable price
        '''
        return obj.total_price

    def due_balance(self, obj):
        '''Return due balance for the individual sale.

        Args:
            obj (Sale): Sale object

        Returns:
            float: Due balance for individual sale.
        '''
        return obj.due_balance

    def cheque_balance(self, obj):
        '''Return cheque balance for the individual sale.

        Args:
            obj (Sale): Sale object

        Returns:
            float: cheque balance for individual sale.
        '''
        return obj.cheque_balance

    def amount_received(self, obj):
        '''Return cash received for the individual sale.

        Args:
            obj (Sale): Sale object

        Returns:
            float: cash received for individual sale.
        '''
        return obj.amount_received
    amount_received.short_description = 'Cash Balance'

    def _location(self, obj):
        '''Return location for the individual sale performed.

        Args:
            obj (Sale): Sale object

        Returns:
            (float, float) | str: (Lat, Long) | Reverse Geocoded address
        '''
        latitude = obj.location[1]
        longitude = obj.location[0]

        geo_setting = GeoCodingSettings.load()

        if geo_setting.sale_location:
            import reverse_geocoder as rg
            result = rg.search((latitude, longitude))
            repr = '{}, {}, {}, {}'.format(
                result[0]["name"],
                result[0]["admin2"],
                result[0]["admin1"],
                result[0]["cc"],
            )
            return repr
        else:
            return f'{round(latitude,2)}, {round(longitude,2)}'
    _location.short_description = '(Lat, Long)'

    def sale_items(self, obj):
        '''Returns Text string separated by comma for sale items for an
        individual sale.

        Args:
            obj (Sale): Sale object

        Returns:
            Text string: Text string separated by comma for sale items.
        '''
        items = []

        for sale in obj.sales.all():
            items.append(f'{sale.egg_type} ({sale.quantity})')

        return ', '.join(items)
    sale_items.short_description = 'Sale Items'
