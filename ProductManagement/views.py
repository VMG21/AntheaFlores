from django.shortcuts import render, redirect
from db.models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def index(request):
    return render(request, 'ProductManagement/index.html')

@staff_member_required
def productCreate(request):
    if request.method == "POST":
        productFormValidation = ProductForm(request.POST, request.FILES)
        if productFormValidation.is_valid():
            productFormValidation.save()
            return redirect('ProductManagement:productList')
        else:
            return render(request, 'ProductManagement/productCreate.html', {
                "productForm": productFormValidation
            })
    else:
        productForm = ProductForm()
        return render(request, 'ProductManagement/productCreate.html', {"productForm": productForm})
    
@staff_member_required
def productList(request):
    return render(request, 'ProductManagement/productList.html', {"productList": Product.objects.all()})

@staff_member_required
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
            return redirect('ProductManagement:productList')
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

@staff_member_required
def productDelete(request, id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('ProductManagement:productList')
