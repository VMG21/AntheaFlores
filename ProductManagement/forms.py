from django import forms
from db import models

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'

class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False)