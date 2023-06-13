from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

ORDER_STATES = [
    ("Cart", "Cart"), 
    ("Confirmado", "Confirmado"),
    ("Enviado", "Enviado"),
    ("Entregado", "Entregado"),
]

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(max_length=500,verbose_name="Descripción")
    image = models.ImageField(upload_to='uploads/product/img', default="", verbose_name="Imagen")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Precio (MXN)")

    def __str__(self):
        return self.name
    
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # The is another separate table for clients.
    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    first_name = models.CharField("Nombre(s)", max_length=200)
    last_name = models.CharField("Apellidos", max_length=200)
    phone_number = models.CharField(
        "Teléfono", max_length=15, unique=True, null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    pass

    class meta:
        pass

    objects = UserManager()

    def _str_(self):
        return self.email, self.first_name


class State(models.Model):
    name = models.CharField("Estado", max_length=100)

    def __str__(self):
        return self.name


class Municipally(models.Model):
    name = models.CharField("Municipio", max_length=100)

    def __str__(self):
        return self.name


class DeliveryAddress(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Nombre", max_length=100)
    internalNumber = models.PositiveIntegerField(
        "Numero Interior", blank=True, null=True)
    outdoorNumber = models.PositiveIntegerField("Numero Exterior")
    street = models.CharField("Calle", max_length=200)
    district = models.CharField(
        "Colonia", max_length=200, blank=True, null=True)
    postalCode = models.PositiveIntegerField("Código Postal")
    municipally = models.ForeignKey(Municipally, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    reference = models.CharField(
        "Reference", max_length=200, blank=True, null=True)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street} # {self.outdoorNumber}, {self.state}, {self.municipally}"

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATES, max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    total = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)
    address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
    
    

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name 
