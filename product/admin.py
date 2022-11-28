from django.contrib import admin
from .models import Product, Client
from django.utils.html import mark_safe
from django.db.models import F

@admin.action(description="Increase stock by 50 units")
def increase_stock(modeladmin, request, queryset):
    queryset.update(stock=F('stock')+50)
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [increase_stock]
# Register your models here.
admin.site.register(Product, ProductAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'list_of_categories')
    def list_of_categories(self,obj):
        to_return = ''
        for sing in obj.interested_in.all():
            to_return += sing.name+", "
        return mark_safe(to_return[:-2])

admin.site.register(Client, ClientAdmin)

