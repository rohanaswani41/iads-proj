from django.db import models
import datetime
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, default='Windsor')

    def __str__(self):
        return self.name + self.warehouse

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, default="")
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.category) + self.name + str(self.price) + str(self.stock) + self.description
    
    def refill(self):
        self.stock += 100

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=100, default=-1)
    avatar = models.ImageField('profile picture', upload_to='static/', null=True, blank=True)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.avatar

class Client(User):
    PROVINCE_CHOICES = [ ('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'),]
    company = models.CharField(max_length=50, blank=True, default="")
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):        
        
        return self.company + self.shipping_address + self.city + self.province + str(self.interested_in)

class Order(models.Model):
    ORDER_STATUS_CHOICES = [(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'Order Shipped'), (3, 'Order Delivered')]
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    order_status = models.IntegerField(default=1, choices=ORDER_STATUS_CHOICES)
    status_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.product) + str(self.client) + str(self.num_units) + str(self.order_status) + str(self.status_date)

    def total_cost(self):
        return self.product.price * self.num_units

