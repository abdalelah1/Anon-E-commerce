from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def loginpage(request):
     if request.method=='POST':
           username=request.POST['username']
           password=request.POST['password']
           user=authenticate(request,username=username,password=password)
           if user is not None: 
                 login(request,user)
                 return redirect('store')
     context={'request':request}
     return render(request,'store/login.html',context)

def RegisterUser(request):
      context=[]
      return render(request,'store/login.html',context)

def store(request):
     if request.user.is_authenticated:
            customer=request.user.customers
            baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
            items=baskets.basket_details_set.all()
            basketItem=baskets.get_cart_items
     else :
            items=[]
            baskets={'get_cart_total':0,'get_cart_items':0 }
            basketItem=baskets['get_cart_items']

     products=Product.objects.all()
     
     context={'products':products,'basketItem':basketItem}
     return render(request,'store/stroe.html',context)
@login_required(login_url='login_Signup')
def basket(request):
        if request.user.is_authenticated:
                customer=request.user.customers
                baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
                items=baskets.basket_details_set.all()
                basketItem=baskets.get_cart_items
        else :
                items=[]
                baskets={'get_cart_total':0,'get_cart_items':0 }
                basketItem=baskets['get_cart_items']
        context={'items':items,'basket':baskets,'basketItem':basketItem }
        return render(request,'store/basket.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId = data['prodcutid']
    action=data['action']
    print('productId',productId)
    print('action',action)
    customer=request.user.customers
    product=Product.objects.get(id=productId)
    print('product 1212',product)
    basket,created=Basket.objects.get_or_create(basket_customer_fk=customer) 
    basket_details,created=Basket_Details.objects.get_or_create(basket_details_basket_fk=basket,
                                                                basket_details_product_fk=product,
                                                                basket_datails_product_price=product.Product_price,
                                                                )
    if action=='add':
        basket_details.basket_details_product_count +=1
    elif action=='remove':
        basket_details.basket_details_product_count -=1
    basket_details.save()
    if basket_details.basket_details_product_count<=0:
        basket_details.delete()
    return JsonResponse('hello world',safe=False)

def SearchProduct(request):
     if request.user.is_authenticated:
                customer=request.user.customers
                baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
                items=baskets.basket_details_set.all()
                basketItem=baskets.get_cart_items
     else :
                items=[]
                baskets={'get_cart_total':0,'get_cart_items':0 }
                basketItem=baskets['get_cart_items']

     query=request.POST['search']
     products=Product.objects.all()
     product=products.filter(Product_name__contains=query)

     context={'products':product,'basketItem':basketItem}
     return render(request,'store/stroe.html',context)

def Signup(request):
      newuser=User.objects.create_user()    
def view_item(request,product_id):
    if request.user.is_authenticated:
            customer=request.user.customers
            baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
            items=baskets.basket_details_set.all()
            basketItem=baskets.get_cart_items
    else :
            items=[]
            baskets={'get_cart_total':0,'get_cart_items':0 }
            basketItem=baskets['get_cart_items']

    print('productId',product_id)
    products=Product.objects.get(id=product_id)
    print("products:",products)
    print("products1:",products)
    context=[]
    context={'products':products,'basketItem':basketItem}
    return render(request,'store/details.html',context)