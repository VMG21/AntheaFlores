from datetime import date
import json
import time
from Catalog.forms import OrderForm
from db.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from db.models import Product

# Create your views here.
def index(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if Order.objects.filter(client=request.user, status="Carrito").exists():
            order = Order.objects.get(client=request.user, status="Carrito")
            orderProducts = OrderProduct.objects.filter(order=order)
            cartCount = orderProducts.count()
        else:
            return render(request, 'Catalog/index.html',{
                'cartCount': 0,
            })
        return render(request, 'Catalog/index.html',{
            'cartCount': cartCount,
        })
    return render(request, 'Catalog/index.html',{
        'cartCount': 0,
    })
 
def getCards(request):
    time.sleep(1)
    json_data = json.loads(request.body)
    search = json_data['jsonBody']['search']
    print(search)
    if search == "" or search == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=search)
    return render(request, 'Catalog/cards.html',{
        "products": products
    })

@login_required
def add_product_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        # Si ya existe el carrito:
        if Order.objects.filter(client=request.user, status="Carrito").exists():
            order = Order.objects.get(client=request.user, status="Carrito")
            # Si ya existe el orderProduct:
            if OrderProduct.objects.filter(order=order, product=product).exists():
                orderProduct = OrderProduct.objects.get(order=order, product=product)
                orderProduct.quantity += 1
                orderProduct.subtotal += product.price
                orderProduct.save()
            # No existe el orderProduct:
            else:
                orderProduct = OrderProduct.objects.create(order=order, product=product, quantity=1, subtotal=product.price*1)
                orderProduct.save()
            # Actualizamos el total del carrito:
            if order.total == None:
                order.total = 0
            order.total += orderProduct.subtotal
            order.save()
        # No existe el carrito:
        else:
            order = Order.objects.create(client=request.user, status="Carrito", total=0, ordered_date=date.today())
            orderProduct = OrderProduct.objects.create(order=order, product=product, quantity=1, subtotal=product.price*1)
            orderProduct.save()
            if order.total == None:
                order.total = 0
            order.total += orderProduct.subtotal
            order.save()
        return redirect('Catalog:index')

def getCart(request):
    if request.user.is_authenticated and not request.user.is_staff:
         if Order.objects.filter(client=request.user, status="Carrito").exists():
            order = Order.objects.get(client=request.user, status="Carrito")
            orderProducts = OrderProduct.objects.filter(order=order)
            deliveryAddress = DeliveryAddress.objects.filter(client=request.user)
            return render(request, 'Catalog/cart.html',{
                'orderProducts': orderProducts,
                'order': order,
                'deliveryAddress': deliveryAddress,
                'form': OrderForm()
            })         
    return redirect('Catalog:index')

def orderProductDelete(request, orderProduct_id):
    if request.method == "POST":
        orderProduct = OrderProduct.objects.get(id=orderProduct_id)
        order = Order.objects.get(id=orderProduct.order.id)
        order.total -= orderProduct.subtotal
        order.save()
        orderProduct.delete()
        return redirect('Catalog:getCart')
    
def orderResume(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if Order.objects.filter(client=request.user, status="Carrito").exists():
            order = Order.objects.get(client=request.user, status="Carrito")
            orderProducts = OrderProduct.objects.filter(order=order)
            return render(request, 'Catalog/resume.html',{
                'orderProducts': orderProducts,
                'order': order,
            })         
    return redirect('Catalog:index')