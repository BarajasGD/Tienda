import imp
from django.shortcuts import render,redirect
from core.forms import *
from django.contrib import messages
from core.models import *


# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'core/index.html',{'products':products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('True')
            form.save()
            print("Data Saved Succesfully")
            messages.success(request,"Product Added Succesfully")
            return redirect('/')
        else:
            print("Not Working")
            messages.info("Product is not Added")
    else:
        form = ProductForm()
    return render(request,'core/add_product.html',{'form':form})