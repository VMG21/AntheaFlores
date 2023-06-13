from django import forms


class ClientSearchForm(forms.Form):
    search = forms.CharField(
        label="Nombre(s)", max_length=200, required=False
    )
    
class OrderSearchForm(forms.Form):
    search = forms.CharField(
        label="Nombre(s)", max_length=200, required=False
    )

class OrderStatusChangeForm(forms.Form):
    order_id = forms.IntegerField(
        label="ID del pedido", required=True
    )
    status = forms.ChoiceField(
        label="Estado del pedido", choices=(
            ("Carrito", "Carrito"), 
            ("Confirmado", "Confirmado"),
            ("Enviado", "Enviado"),
            ("Entregado", "Entregado"),
        )
    )