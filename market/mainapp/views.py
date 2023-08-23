from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .recommensation_system import show_recommendations1,show_recommendations
from django.contrib.auth import logout
from django.urls import reverse     
# Create your views here.
def loginpage(request):
     if request.method=='POST':
           username=request.POST['username']
           password=request.POST['password']
           user=authenticate(request,username=username,password=password)
           if user is not None: 
                  if request.user.is_staff:
        # User is an admin
        # Add your admin logic here
                        return redirect('admin')
                  login(request,user)
                  return redirect('store')
     context={'request':request}
     return render(request,'store/login.html',context)

def RegisterUser(request):
      context={}
      return render(request,'store/register.html',context)
def checkout(request):
      user = request.user.customers
      shipping_info = None 
      if request.user.is_authenticated:
                customer=request.user.customers
                baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
                items=baskets.basket_details_set.all()
                basketItem=baskets.get_cart_items
                
      else :
                items=[]
                baskets={'get_cart_total':0,'get_cart_items':0 }
                basketItem=baskets['get_cart_items']
      context={'items':items,'basket':baskets,'basketItem':basketItem,'user':user }
      if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        if not shipping_info:
            shipping_info = ShippingInfo(customer=customer)
        shipping_info.address = address
        shipping_info.city = city
        shipping_info.state = state
        shipping_info.country = country
        shipping_info.save()   
                # Create a new order instance
        
        order = Orders(customer=customer, total_price=baskets.get_cart_total)
        order.save()
        
        for item in items:
            order_details = Order_Details(
                price=item.basket_datails_product_price,
                count=item. basket_details_product_count,
                product=item.basket_details_product_fk,
                order=order,
            )
            order_details.save()
        
        baskets.basket_details_set.all().delete()
        
        return redirect('main_page')
     

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
@login_required(login_url='login')
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

     query=request.POST['search'].lower()
     products=Product.objects.all()
     product=products.filter(Product_name__icontains=query)

     context={'products':product,'basketItem':basketItem}
     return render(request,'store/stroe.html',context)

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
      if request.user.is_authenticated:
            customer=request.user.customers
            baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
            items=baskets.basket_details_set.all()
            basketItem=baskets.get_cart_items
            orders = get_order_history(customer)
            print ("from home page ", orders)
      else :
            items=[]
            baskets={'get_cart_total':0,'get_cart_items':0 }
            basketItem=baskets['get_cart_items']  
            orders=[]
      print ("from home page ", orders)
      context=[]
      context={'CurrentOrders':orders}   
      return render(request,'store/index.html',context)
def main_page (request):
      if request.user.is_authenticated:
            customer=request.user.customers
            baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
            items=baskets.basket_details_set.all()
            basketItem=baskets.get_cart_items
            orders = get_order_history(customer)
      else :
            items=[]
            baskets={'get_cart_total':0,'get_cart_items':0 }
            basketItem=baskets['get_cart_items']
            orders=[]
      Categories=Category.objects.all()
      Offer=Offers()
      context=[]
      latest_product =new_product()
      context={"latest_product":latest_product,"Offers":Offer,"Categories":Categories,'basketItem':basketItem,'CurrentOrders':orders}
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
            if request.user.is_authenticated:
                customer=request.user.customers
                baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
                items=baskets.basket_details_set.all()
                basketItem=baskets.get_cart_items
            else :
                items=[]
                baskets={'get_cart_total':0,'get_cart_items':0 }
                basketItem=baskets['get_cart_items']
            products=Product.objects.filter(product_category_fk=category_id)
            context=[]
            context={"products":products,'basketItem':basketItem}
            return render(request,'store/mainProduct.html',context)
def order_history(request):
      if request.user.is_authenticated:
                customer=request.user.customers
                baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
                items=baskets.basket_details_set.all()
                basketItem=baskets.get_cart_items
                orders = Orders.objects.filter(customer=customer)
                CurrentOrders=get_order_history(customer)
                
      else :
                items=[]
                baskets={'get_cart_total':0,'get_cart_items':0 }
                basketItem=baskets['get_cart_items']
      context={'items':items,'basket':baskets,'basketItem':basketItem,'user':request.user, 'orders':orders,'CurrentOrders':CurrentOrders }

      return render(request,'store/order_history.html',context)
def get_order_history(customer):
    
    orders = Orders.objects.filter(customer=customer).order_by('-data_added')[:2]
    print("order is ",orders)
    return orders
def order_details(request,orderID):
      if request.user.is_authenticated:
            customer=request.user.customers
            baskets,created=Basket.objects.get_or_create(basket_customer_fk=customer)
            items=baskets.basket_details_set.all()
            basketItem=baskets.get_cart_items
            order = Orders.objects.get(id=orderID)
            details = order.order_details_set.all()
            print("details",details)
            
      else :
            items=[]
            baskets={'get_cart_total':0,'get_cart_items':0 }
            basketItem=baskets['get_cart_items']     
      context={'items':items,'basket':baskets,'basketItem':basketItem,'user':request.user, 'details':details,'order':order }
  
      return render(request,'store/order_details.html',context)
def register_customer(request):
  
    print("from register")
    if request.method == 'POST':
        # Get form data
        customer_name = request.POST['customer_name']
        customer_birth_date = request.POST['customer_birth_date']
        customer_mobile_number = request.POST['customer_mobile_number']
        customer_gender = request.POST['customer_gender']
        customer_email = request.POST['customer_email']
      #   address = request.POST['address']
      #   city = request.POST['city']
      #   state = request.POST['state']
      #   country = request.POST['country']
        username = request.POST['username']
        password = request.POST['password']
        
        # Create new user
        user = User.objects.create_user(username=username, password=password)
        
        # Create new customer
        customer = Customers.objects.create(
            customer_name=customer_name,
            customer_Birth_date=customer_birth_date,
            customer_Mobile_number=customer_mobile_number,
            customer_gender=customer_gender,
            customer_email=customer_email,
            custome_fk=user
        )
        
        # Create new shipping info
      #   shipping_info = ShippingInfo.objects.create(
      #       customer=customer,
      #       address=address,
      #       city=city,
      #       state=state,
      #       country=country
      #   )
        messages.success(request, 'Your account has been created successfully.')

        # Redirect to success page
        return redirect('main_page')
    else:
          return render(request, 'store/register.html')
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Customers

def log_in(request):
    if request.method == 'POST':
        username = request.POST['user-name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                # User is an admin
                # Add your admin logic here
                return redirect(reverse('admin:index')) # Redirect to admin page
            
            # User is a customer
            # Check if the customer exists in the Customers model
            if Customers.objects.filter(custome_fk=user).exists():
                login(request, user)
                return redirect('main_page')  # Redirect to customer page

    context = {'request': request}
    return render(request, 'store/final_login.html', context)

def logout_view(request):
    logout(request)
    return redirect('main_page')