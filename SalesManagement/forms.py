from django import forms


class ClientSearchForm(forms.Form):
    search = forms.CharField(
        label="Nombre(s)", max_length=200, required=False
    )
    