from django import forms
from product.models import Order, User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm

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

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class InterestForm(forms.Form):
    
    CHOICES = (('1', 'Yes'), ('0', 'No'))   
    #model = Product
    #fields = ["interested","stock","comments"]
    interested = forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES, initial="1")
    #interested = forms.ChoiceField(widget=forms.RadioSelect)
    quantity = forms.IntegerField(initial=1, label="quantity")
    comments = forms.CharField(widget=forms.Textarea,label=mark_safe("<br/>Additional Comments"))
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    class Meta:
        model = User
        fields = ("email","username","password1","password2")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class ProfilePhotoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ProfilePhotoForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False
    avatar = forms.ImageField(label="Upload Profile Photo")

class ForgotPassword(forms.Form):
    username = forms.CharField(label="Enter Username")

