from django.shortcuts import redirect, render
from db.models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def userProfile(request):
    return render(request, 'AccountManagement/userProfile.html')
@login_required
def myAccount(request):
    client = request.user
    return render(request, 'AccountManagement/myAccount.html',{
        'client': client
    })
@login_required
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
    
@login_required    
def addressList(request):
    if request.method =="POST":
        form = DeliveryAddressSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            query = (
                Q(street__icontains=search) |
                Q(district__icontains=search) |
                Q(municipally__name__icontains=search) |
                Q(state__name__icontains=search) |
                Q(reference__icontains=search)
            )
            if search.isdigit():
                query = query | Q(internalNumber=search) | Q(outdoorNumber=search) | Q(postalCode=search)
            
            if search == "":
                addressList = DeliveryAddress.objects.filter(disable=False, client=request.user)
            else:
                addressList = DeliveryAddress.objects.filter(query & Q(client=request.user) & Q(disable=False))

            return render(request, 'AccountManagement/deliveryAddressList.html', {
                "addressList": addressList,
                 "form": form
            })
    else:
        addressList = DeliveryAddress.objects.filter(client=request.user, disable=False)
        return render(request, 'AccountManagement/deliveryAddressList.html',{
            'addressList': addressList
        })


@login_required
def addressCreate(request):
    if request.method == "POST":
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            delivery_address = form.save(commit=False)
            delivery_address.client = request.user
            delivery_address.save()
            return redirect('AccountManagement:addressList')
        else:
            return render(request, 'AccountManagement/addressCreate.html', {'form': form})
    else:
        form = DeliveryAddressForm()
        return render(request, 'AccountManagement/addressCreate.html', {'form': form})

@login_required
def addressModify(request, id):
    address = DeliveryAddress.objects.get(id=id)
    if request.method == "POST":
        form = DeliveryAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('AccountManagement:addressList')
        else:
            return render(request, 'AccountManagement/addressModify.html', {'form': form, 'address': address})
    else:
        form = DeliveryAddressForm(instance=address)
        return render(request, 'AccountManagement/addressModify.html', {'form': form, 'address': address})

@login_required
def addressDelete(request, id):
    address = DeliveryAddress.objects.get(id=id)
    if request.method == "POST":
        address.disable=True
        address.save()
        return redirect('AccountManagement:addressList')
    
    