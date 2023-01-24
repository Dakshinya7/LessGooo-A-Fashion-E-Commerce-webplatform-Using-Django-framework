from itertools import product
from unicodedata import category
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages


#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles})


#def product_detail(request):
 #return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product})

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user = user, product = product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        return render(request, 'app/addtocart.html',{'carts':cart})


def buy_now(request):
 return render(request, 'app/buynow.html')

#def profile(request):
 #return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

#def change_password(request):
 #return render(request, 'app/changepassword.html')

def mobile(request, data = None):
 if data == None:
    mobiles = Product.objects.filter(category='M')
 elif data == 'H&M' or data == 'Roadster':
    mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'Below':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=1000)
 return render(request, 'app/mobile.html', {'mobiles': mobiles})

#def login(request):
 #return render(request, 'app/login.html')



#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congrats! You have registered successfully!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})


def checkout(request):
 return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congrats! Profile updated successfully.')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

def orderdelivered(request):
        emps = ProfileView.objects.all()
        cou= emps.count()

        return render(request, 'home.html', {'cou':cou,})
