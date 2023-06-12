from django import forms
from db import models

class DeliveryAddress(forms.ModelForm):
    class Meta:
        model = models.DeliveryAddress
        fields = '__all__'
