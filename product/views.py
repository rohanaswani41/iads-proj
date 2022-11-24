from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from django.shortcuts import render

# Import necessary classes
from .models import Category, Product
from .forms import OrderForm, InterestForm

# Import necessary classes and models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'index.html', {'cat_list': cat_list, 'user_name':"batman"})

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'product/login.html')

    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

def about(request):
    return render(request, 'about.html', {'user_name':"batman"})

def detail_view(request, cat_no):
    category = Category.objects.filter(name=cat_no).first()
    products = Product.objects.filter(category__name=cat_no).all()
    return render(request, 'detail0.html', {'cat_list': category, 'prod_list': products, 'user_name':"batman"})

def products_view(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'products.html', {'prodlist': prodlist, 'user_name':"batman"})

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                prod = order.product
                prod.stock = prod.stock - order.num_units
                prod.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'order_response.html', {'msg': msg, 'user_name':"batman"})

    else:
        form = OrderForm()
        return render(request, 'placeorder.html', {'form':form, 'msg':msg,'prodlist':prodlist, 'user_name':"batman"})

def productdetail(request, prod_id):
    

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            product = Product.objects.filter(name=prod_id).first()
            clean_data = form.cleaned_data
            if clean_data['interested'] == '1':
                product.interested += 1
                product.save(update_fields=['interested'])
            
            url = reverse('myapp:index')
            return HttpResponseRedirect(url)

    else:
        prodlist = Product.objects.filter(name=prod_id).all()
        form = InterestForm()
        return render(request, 'products.html', {'form':form, 'prodlist': prodlist, 'user_name':"batman", "stock": prodlist[0].stock})
