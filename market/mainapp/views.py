from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .recommensation_system import show_recommendations1,show_recommendations
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
def checkout(request):
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
      return render(request,'store/checkout.html',context)
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
    products=Product.objects.get(id=product_id)
#     cluster_id,cluster_products=show_recommendations1(products.Product_description)
#     print("cluser",cluster_id,"cluster_products",cluster_products)
    recommedationProducts=show_recommendations(products.Product_description)
    recommedationProducts = Product.objects.filter(Product_asin__in=recommedationProducts[1])
    print('matching_products',products)
    context=[]
    context={'products':products,'basketItem':basketItem,'recommedationProducts':recommedationProducts}
    return render(request,'store/details.html',context)

def home (request):
      return render(request,'store/index.html')
def main_page (request):
      if request.user.is_authenticated:
            customer=request.user.customers
            baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
            items=baskets.basket_details_set.all()
            basketItem=baskets.get_cart_items
      else :
            items=[]
            baskets={'get_cart_total':0,'get_cart_items':0 }
            basketItem=baskets['get_cart_items']
      Categories=Category.objects.all()
      Offer=Offers()
      context=[]
      latest_product =new_product()
      context={"latest_product":latest_product,"Offers":Offer,"Categories":Categories,'basketItem':basketItem}
      return render(request,'store/home.html',context)
def new_product() :
      latest_product=Product.objects.order_by('-product_date_added')[:12]
      
      return latest_product
def Offers():
      allOffers=Offer.objects.all()
      for i in allOffers : 
            print("ii",i)
      return allOffers  
def mainPorduct(request):
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
     context=[]
     context={'products':product,'basketItem':basketItem}
     return render(request,'store/mainProduct.html',context)
def show_category_products(request, category_id):
       products=Product.objects.filter(product_category_fk=category_id)
       context=[]
       context={"products":products}
       return render(request,'store/mainProduct.html',context)