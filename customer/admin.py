from django.contrib import admin
from django.db.models import Sum
from mapbox_location_field.admin import MapAdmin

from core.models import GeoCodingSettings
from sales.models import Sale

from .forms import CreditPaymentForm
from .models import (
    CreditPayment,
    Customer,
    PaymentHistory,
    SaleLocation,
)


@admin.register(Customer)
class CustomerAdmin(MapAdmin, admin.ModelAdmin):
    '''Admin View for Customer'''

    list_display = (
        'name',
        'shop_name',
        'vat_no',
        '_location',
        'total_paid',
        'cash_paid',
        'cheque_paid',
        'due_balance',
        'sale_location',
    )

    search_fields = ('name', )

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

        if geo_setting.customer_location:
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

    _location.short_description = 'Customer Location'

    def total_paid(self, obj):
        ''' Returns total paid amount by customer.
        '''

        total_paid = 0

        if Sale.objects.filter(customer=obj).exists():
            customer_sales = Sale.objects.filter(customer=obj)

            for customer_sale in customer_sales:
                amount_paid = customer_sale.payments.all().exclude(
                    type='CR').aggregate(sum=Sum('amount')).get('sum') or 0.0
                total_paid += amount_paid

        # Cumulate paid credit amount and
        # add to total cash paid.
        if CreditPayment.objects.filter(customer=obj).exists():
            credit_payment = CreditPayment.objects.filter(customer=obj)

            for payment in credit_payment:
                paid_credit_amount = payment.amount
                total_paid += paid_credit_amount

        return total_paid

    def cash_paid(self, obj):
        ''' Returns total cash paid amount by customer.
        '''

        total_cash_paid = 0

        if Sale.objects.filter(customer=obj).exists():
            customer_sales = Sale.objects.filter(customer=obj)

            for customer_sale in customer_sales:
                cash_paid = customer_sale.amount_received
                total_cash_paid += cash_paid

        # Cumulate paid credit amount and
        # add to total cash paid.
        if CreditPayment.objects.filter(customer=obj).exists():
            credit_payment = CreditPayment.objects.filter(customer=obj)

            for payment in credit_payment:
                paid_credit_amount = payment.amount
                total_cash_paid += paid_credit_amount

        return total_cash_paid

    def cheque_paid(self, obj):
        ''' Returns total cheque paid amount by customer.
        '''

        if Sale.objects.filter(customer=obj).exists():
            customer_sales = Sale.objects.filter(customer=obj)
            total_cheque_paid = 0

            for customer_sale in customer_sales:
                cheque_paid = customer_sale.cheque_balance
                total_cheque_paid += cheque_paid
            return total_cheque_paid
        else:
            return 0.0

    def due_balance(self, obj):
        ''' Returns total due balance to be paid by customer.
        '''

        total_due_balance = 0

        # Cumulate credit transaction processed by
        # client from individual sales.
        if Sale.objects.filter(customer=obj).exists():
            customer_sales = Sale.objects.filter(customer=obj)

            for customer_sale in customer_sales:
                due_balance = customer_sale.due_balance
                total_due_balance += due_balance

        # Cumulate paid credit amount and
        # subtract from the total due balance.
        if CreditPayment.objects.filter(customer=obj).exists():
            credit_payment = CreditPayment.objects.filter(customer=obj)

            for payment in credit_payment:
                paid_credit_amount = payment.amount
                total_due_balance -= paid_credit_amount
        return total_due_balance


@admin.register(SaleLocation)
class SaleLocationAdmin(admin.ModelAdmin):
    '''Admin View for SaleLocation'''

    list_display = ('location', )


@admin.register(CreditPayment)
class CreditPaymentAdmin(admin.ModelAdmin):
    '''Admin View for CreditPayment'''

    list_display = (
        'customer',
        'amount',
        'created',
    )

    list_filter = (
        'created',
        'customer',
    )

    date_hierarchy = 'created'

    form = CreditPaymentForm


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    '''Admin View for PaymentHistory'''

    list_display = (
        'customer',
        'amount',
        'payment_type',
        'created',
        'description',
    )
    list_filter = (
        'payment_type',
        'created',
        'amount',
    )

    readonly_fields = ('description', )
    search_fields = ('customer', )
    date_hierarchy = 'created'
    ordering = (
        '-created',
        '-modified',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
