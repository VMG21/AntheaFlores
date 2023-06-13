from django import forms
from db import models

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryAddress
        fields = [ 'street', 'outdoorNumber', 'internalNumber', 'district', 'municipally', 'state', 'reference', 'postalCode']


class OrderSearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)

class DeliveryAddressSearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)
    