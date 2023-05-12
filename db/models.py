from django.conf import settings
from django.db import models

ORDER_STATES = [("Cart", "Cart"), ("Confirmado", "Confirmado")]

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(max_length=500,verbose_name="Descripción")
    image = models.ImageField(upload_to='uploads/product/img', default="", verbose_name="Imagen")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Precio (MXN)")

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATES, max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    total = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)

    def __str__(self):
        return self.user.username

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name 
