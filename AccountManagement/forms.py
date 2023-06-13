from django import forms
from db import models

class DeliveryAddress(forms.ModelForm):
    class Meta:
        model = models.DeliveryAddress
        fields = '__all__'

class OrderSearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)
    