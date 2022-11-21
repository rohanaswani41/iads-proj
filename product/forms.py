from django import forms
from product.models import Order, Product
from django.utils.safestring import mark_safe

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["client" ,"product", "num_units"]
        widgets = {
            "client": forms.RadioSelect
        }
        labels ={
            "num_units":"Quantity"
        }

class InterestForm(forms.Form):
    
    CHOICES = (('1', 'Yes'), ('0', 'No'))   
    #model = Product
    #fields = ["interested","stock","comments"]
    interested = forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES, initial="1")
    #interested = forms.ChoiceField(widget=forms.RadioSelect)
    quantity = forms.IntegerField(initial=1, label="quantity")
    comments = forms.CharField(widget=forms.Textarea,label=mark_safe("<br/>Additional Comments"))
    