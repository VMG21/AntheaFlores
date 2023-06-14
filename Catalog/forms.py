from django import forms
from db import models

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['address']