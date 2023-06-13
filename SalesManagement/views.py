from django.shortcuts import render, redirect
from db.models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q



@staff_member_required
def clientList(request):
    if request.method == "POST":
        form = ClientSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['search'] == "":
                clientList = User.objects.filter(is_staff=False)
            else:
                clientList = User.objects.filter(
                    (Q (first_name__icontains=form.cleaned_data['search']) |
                    Q (last_name__icontains=form.cleaned_data['search']) |
                    Q (email__icontains=form.cleaned_data['search']) |
                    Q (phone_number__icontains=form.cleaned_data['search'])) &
                    Q (is_staff=False) & Q (is_active=True)
                )
            return render(request, 'SalesManagement/clientList.html', {
                "clientList": clientList,
                 "form": form
            })
    else:
        form = ClientSearchForm()
        return render(request, 'SalesManagement/clientList.html', {
            "clientList": User.objects.filter(is_staff=False, is_active=True ),
            "form": form
        })

@staff_member_required
def clientBlock(request, id):
    if request.method == "POST":
        client = User.objects.get(id=id)
        client.is_active = False
        client.save()
        return redirect('SalesManagement:clientList')


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def orderList(request):
    if request.method == "POST":
        form = OrderSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search == "":
                orderList = Order.objects.exclude(status__in=['Entregado', 'Carrito']).order_by('-ordered_date')
            else:
                orderList = Order.objects.filter(
                    Q(status__icontains=search) |
                    Q(address__street__icontains=search) |
                    (Q(total=search) if search.isdigit() else Q())
                ).exclude(status__in=['Entregado', 'Carrito']).order_by('-ordered_date')

            return render(request, 'SalesManagement/orderList.html', {
                "orderList": orderList,
                 "form": form
            })
    else:
        form = OrderSearchForm()
        return render(request, 'SalesManagement/orderList.html', {
            "orderList": Order.objects.exclude(status__in=['Entregado', 'Carrito']).order_by('-ordered_date'),
            "form": form
        })

    
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def orderHistory(request):
    if request.method == "POST":
        form = OrderSearchForm(request.POST)
        form2 = OrderStatusChangeForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search == "":
                orderList = Order.objects.filter(status='Entregado')
            else:
                orderList = Order.objects.filter(
                    Q(status__icontains=search) |
                    Q(address__street__icontains=search) |
                    (Q(total=search) if search.isdigit() else Q()),
                    status='Entregado'
                )
                
            return render(request, 'SalesManagement/orderHistory.html', {
                "orderList": orderList.order_by('-ordered_date'),
                "form": form,
                "form2": form2
            })
    else:
        form = OrderSearchForm()
        form2 = OrderStatusChangeForm()
        return render(request, 'SalesManagement/orderHistory.html', {
            "orderList": Order.objects.filter(status='Entregado').order_by('-ordered_date'),
            "form": form,
            "form2": form2
        })

@staff_member_required
def orderStatusChange(request):
    if request.method == "POST":
        form = OrderStatusChangeForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(id=form.cleaned_data['order_id'])
            order.status = form.cleaned_data['status']
            order.save()
            return redirect('SalesManagement:orderList')
    