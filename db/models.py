from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='uploads/product/img', default="", blank=True, null=True)

    def __str__(self):
        return self.name