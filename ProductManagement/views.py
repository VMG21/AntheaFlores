from django.shortcuts import render, redirect
from db.models import *
from .forms import *


def productCreate(request):
    if request.method == "POST":
        productFormValidation = ProductForm(request.POST, request.FILES)
        if productFormValidation.is_valid():
            productFormValidation.save()
            return redirect('Catalog:index')
        else:
            return render(request, 'ProductManagement/productCreate.html', {
                "productForm": productFormValidation
            })
    else:
        productForm = ProductForm()
        return render(request, 'ProductManagement/productCreate.html', {"productForm": productForm})

def productList(request):
    return render(request, 'ProductManagement/productList.html', {"productList": Product.objects.all()})

def productModify(request, id):
    #Lista de objetos
    allProducts = Product.objects.all()
    # products = Product.objects.filter()

    #Objeto
    product = Product.objects.get(id=id)

    if request.method == "POST":
        productFormValidation = ProductForm(request.POST, request.FILES, instance=product)
        if productFormValidation.is_valid():
            productFormValidation.save()
            return redirect('Catalog:index')
        else:
            return render(request, 'ProductManagement/productModify.html', {
                "product": product,
                "allProducts": allProducts,
                "productForm": productForm,
            })
    else:
        
        productForm = ProductForm(instance=product)
        return render(request, 'ProductManagement/productModify.html', {
            "product": product,
            "allProducts": allProducts,
            "productForm": productForm,
            })
    
def productDelete(request, id):
    product = Product.objects.get(id)
    product.delete()
    return redirect('/productList.html')
