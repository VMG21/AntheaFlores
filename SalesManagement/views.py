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
