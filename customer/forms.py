from django import forms

from .models import CreditPayment


class CreditPaymentForm(forms.ModelForm):
    ''' Form for filling Payment processed by Customer. '''
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not amount > 0:
            return forms.ValidationError(
                f'Amount: {amount} should be greater than zero.'
            )
        return amount

    class Meta:
        model = CreditPayment
        fields = (
            'customer',
            'amount',
        )
