from django.shortcuts import render, redirect
from .forms import UserCreateForm
# Create your views here.
def CreateAccount(request):
    if request.method == "POST":
        formValidation = UserCreateForm(request.POST)
        if formValidation.is_valid():
            formValidation.save()
            return redirect('login')
        else:
            return render(request, "registration/createAccount.html",{
                "form":formValidation
            }) 
            
    form = UserCreateForm
    return render(request, "registration/createAccount.html",{
        "form":form
    })