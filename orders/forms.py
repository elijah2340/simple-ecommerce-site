from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address_line_1',
                  'address_line_2', 'country', 'state', 'city', 'shipping_address',
                  'shipping_country', 'shipping_state', 'shipping_city', 'shipping_address_same_as_billing']

#
# class ApplyCoupon(forms.ModelForm):
#
#     class Meta:
#         model = Order
#         fields = ['coupon']
