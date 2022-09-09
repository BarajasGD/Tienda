import imp
from django.shortcuts import render,redirect
from core.forms import *
from django.contrib import messages
from core.models import *
from django.utils import timezone


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


def product_desc(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html',{'product':product})



def add_to_cart(request, pk):
    # Get that Partiuclar Product of id = pk
    product = Product.objects.get(pk=pk)

    # Create Order item
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )



    # Get Query set of Order Object of Particular User
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added Quantity Item")
            return redirect("product_desc", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to Cart")
            return redirect("product_desc", pk=pk)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to Cart")
        return redirect("product_desc", pk=pk)

