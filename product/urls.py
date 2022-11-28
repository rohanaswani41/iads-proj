"""composeexample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views 
from django.urls import include, path

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index , name='index'),
    path(r'about/', views.about, name='about' ),
    path(r'<str:cat_no>', views.detail_view, name='details'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'products/',views.products_view, name='products_view'),
    path(r'products/<str:prod_id>', views.productdetail, name="productdetail" ),
    path(r'login/', views.user_login, name="login" ),
    path(r'logout/', views.user_logout, name="logout" ),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'register/', views.register, name='register'),
    path(r'profilephoto/', views.profile, name="profile"),
    path(r'forgotpassword/', views.forgot_password, name="forgotpassword")
]

