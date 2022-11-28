from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
# Create your views here.
from django.shortcuts import render, redirect

# Import necessary classes
from .models import Category, Product, Order, MyUser, User
from .forms import OrderForm, InterestForm, CustomUserCreationForm, LoginForm, ProfilePhotoForm, ForgotPassword

# Import necessary classes and models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    sess_time = None
    if "last_login_time" in request.session.keys():
        sess_time = request.session["last_login_time"]
    return render(request, 'index.html', {'cat_list': cat_list, 'user_name':"batman", "last_login_time": sess_time })

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                now = datetime.now()
                request.session["last_login_time"] = now.strftime("%d/%m/%Y %H:%M:%S")
                request.session["name"] = str(user)
                request.session.set_expiry(3600)
                if 'next' not in request.POST:
                    return HttpResponseRedirect(reverse('myapp:index'))
                else:
                    return HttpResponseRedirect(reverse('myapp:myorders'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()
        return render(request, 'product/login.html', { 'form': form})

    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def myorders(request):
    if request.user.is_authenticated:
        list_of_orders = Order.objects.filter(client_id=request.user.id).all()
        return render(request, 'product/orders.html',{"orders":list_of_orders})
    else:    
        return HttpResponseRedirect('/myapp/login/?path=path')

def about(request):
    value = 0
    if "about_visits" not in request.COOKIES.keys():
        value = 1
    else:
        value = int(request.COOKIES["about_visits"])+1
    response = render(request, 'about.html', {'user_name':"batman", "number_of_visits": value })
    response.set_cookie('about_visits', value, max_age=300)
    return response

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


def register(request):
    if  request.method == "POST":
        print(request)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors.as_data())
            return render(request, 'register.html', {'form':form, 'errors':form.errors.as_data()})
        return HttpResponseRedirect(reverse(('myapp:index')))
        

    else:
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form':form })

@login_required
def profile(request):
    if  request.method == "POST":
        form = ProfilePhotoForm(request.POST,request.FILES)
        if form.is_valid():
            myuser = MyUser.objects.filter(username=request.user).first()
            if myuser == None:
                p = MyUser(avatar = request.FILES['avatar'],username=request.user)
                p.save()
            else:
                myuser.avatar = request.FILES['avatar']
                myuser.save()
        return HttpResponseRedirect(reverse(('myapp:profile')))
    else:
        ava = ''
        form = ProfilePhotoForm(request.user)
        myuser = MyUser.objects.filter(username=request.user).first()
        if myuser!=None:
            ava = str(myuser.avatar)
        return render(request, 'profilephoto.html', {'form':form, "photo":ava })

import random
import string    
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def forgot_password(request):
    if  request.method == "POST":
        form = ForgotPassword(request.POST)
        if form.is_valid():
            general = User.objects.filter(username = request.POST['username'])
            otp = get_random_string(8)
            print(otp)
            print(general)
            send_mail("New Password", " <h3>New Password</h3> <p> Your new password is: "+otp +"</p>","info@admin.com",[general.email])
            return HttpResponseRedirect(reverse(('myapp:login')))

    else:
        form = ForgotPassword()
        return render(request, 'forgot_password.html', {'form':form})
