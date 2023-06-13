from django.shortcuts import redirect, render
from db.models import *
from .forms import *
from django.db.models import Q

# Create your views here.

def userProfile(request):
    return render(request, 'AccountManagement/userProfile.html')

def myAccount(request):
    client = request.user
    return render(request, 'AccountManagement/myAccount.html',{
        'client': client
    })

def orderList(request):
    if request.method =="POST":
        form = OrderSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['search'] == "":
                orderList = Order.objects.all()
            else:
                orderList = Order.objects.filter(
                    Q(status__icontains=form.cleaned_data['search']) |
                    Q(address__street__icontains=form.cleaned_data['search']) |
                    Q(total__icontains=form.cleaned_data['search']) 
                
                )
            return render(request, 'AccountManagement/orderList.html', {
                "orderList": orderList,
                 "form": form
            })

    else:  
        orderList = Order.objects.filter(client=request.user)
        return render(request, 'AccountManagement/orderList.html',{
            'orderList': orderList
        })

def addressList(request):
    addressList = DeliveryAddress.objects.filter(client=request.user)
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