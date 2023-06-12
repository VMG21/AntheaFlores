from django.shortcuts import redirect, render
from db.models import *

# Create your views here.

def userProfile(request):
    return render(request, 'AccountManagement/userProfile.html')

def myAccount(request):
    client = request.user
    return render(request, 'AccountManagement/myAccount.html',{
        'client': client
    })

def myPurchases(request):
    orderList = Order.objects.all(client=request.user)
    return render(request, 'AccountManagement/myPurchases.html',{
        'orderList': orderList
    })

def addressList(request):
    addressList = DeliveryAddress.objects.all(client=request.user)
    return render(request, 'AccountManagement/addressList.html',{
        'addressList': addressList
    })

def addressCreate(request):
    if request.method == "POST":
        form = DeliveryAddress(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addressList')
        else:
            return render(request, 'AccountManagement/addressCreate.html', {'form': form})
    else:
        form = DeliveryAddress()
        return render(request, 'AccountManagement/addressCreate.html', {'form': form})
    
def addressModify(request, id):
    address = DeliveryAddress.objects.get(id=id)
    if request.method == "POST":
        form = DeliveryAddress(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('addressList')
        else:
            return render(request, 'AccountManagement/addressModify.html', {'form': form})
    else:
        form = DeliveryAddress(instance=address)
        return render(request, 'AccountManagement/addressModify.html', {'form': form})
    
def addressDelete(request, id):
    address = DeliveryAddress.objects.get(id=id)
    if request.method == "POST":
        address.delete()
        return redirect('addressList')