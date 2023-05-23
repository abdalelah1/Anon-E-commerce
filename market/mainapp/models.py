from django.db import models
from django.contrib.auth.models import User
from datetime import date,datetime
# Create your models here.


class Customers(models.Model):
        customer_name = models.CharField(max_length=30,unique=True)
        customer_Birth_date = models.CharField(max_length=30)
        customer_Mobile_number=models.CharField(max_length=15)
        customer_gender=models.CharField(max_length=4)
        customer_email=models.CharField(max_length=255)
        is_admin = models.BooleanField(default=False)
        custome_fk=models.OneToOneField(User,on_delete=models.CASCADE,null=False)
        def __str__(self) :
                return str(self.id)
class ShippingInfo(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=False)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)
class Category(models.Model):
        Category_name=models.CharField(max_length=100)
        Category_totoal_count=models.IntegerField(default=0)
        Category_icon=models.ImageField(null=True)
        def __str__(self) :
                return str(self.id)
class Product(models.Model):
        Product_name=models.CharField(max_length=1000)
        Product_description=models.CharField(max_length=10000)
        Product_counter=models.IntegerField(default=0,null=True)
        Product_price=models.FloatField()
        Product_brand=models.CharField(max_length=500)
        Product_image=models.ImageField(null=True)
        Product_asin=models.CharField(max_length=500)
        product_category_fk=models.ForeignKey(Category,on_delete=models.CASCADE,null=False)
        product_date_added = models.DateField(default=date.today)
        def __str__(self) :
                return str(self.id)
class Product_Rating(models.Model):
        rating_stars=models.IntegerField()
        rating_description=models.CharField(max_length=100)
        product_rating_product_fk=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
        def __str__(self) :
                return str(self.id)

class Basket(models.Model):
        basket_total_price=models.FloatField(default=0.0)
        basket_customer_fk=models.ForeignKey(Customers,on_delete=models.CASCADE,null=False)
        basket_date = models.DateTimeField(auto_now_add=True, blank=True)
        def __str__(self) :
                return str(self.id)
        @property
        def get_cart_total(self):
            basketitems=self.basket_details_set.all()
            total=sum([item.get_total for item in basketitems])
            return total
        @property
        def get_cart_items(self):
            basketitems=self.basket_details_set.all()
            total=sum([item.basket_details_product_count for item in basketitems])   
            return total
        def confirm_order(self):
                order = Orders.objects.create(customer=self.basket_customer_fk, total_price=self.basket_total_price)
                basket_items = self.basket_details_set.all()
                for item in basket_items:
                        Order_Details.objects.create(product=item.basket_details_product_fk,
                                                        price=item.basket_details_product_fk.Product_price,
                                                        count=item.basket_details_product_count,
                                                        order=order)
                basket_items.delete()

class Basket_Details(models.Model):
        basket_details_product_fk=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
        basket_datails_product_price=models.FloatField()
        basket_details_basket_fk=models.ForeignKey(Basket,on_delete=models.CASCADE,null=False)
        basket_details_product_count=models.IntegerField(default=0)
        def __str__(self) :
                return str(self.id)
        @property
        def get_total(self):
            total =self.basket_details_product_fk.Product_price*self.basket_details_product_count
            return total
        
class Bill(models.Model):
        bill_customer_fk=models.ForeignKey(Customers,on_delete=models.CASCADE,null=False)
        bill_total_price=models.FloatField()
        def __str__(self) :
                return self.id 

class Bill_details(models.Model):
        bill_datails_vat=models.FloatField(default=1.0)
        bill_datails_final_price=models.FloatField()
        bill_details_counter=models.IntegerField()
        bill_details_date=models.CharField(max_length=255)
        bill_details_bill_fk=models.ForeignKey(Bill,on_delete=models.CASCADE)
        def __str__(self) :
                return self.id 

class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_description = models.CharField(max_length=1000)
    offer_discount = models.FloatField()
    offer_before_discount=models.FloatField()
    offer_after_discount = models.FloatField()
    offer_start_date = models.DateField()
    offer_end_date = models.DateField()
    offer_product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    @property 
    def enddate(self):
          end_datetime = datetime.combine(self.offer_end_date, datetime.min.time())
          time_diff = end_datetime - datetime.now()
          days=time_diff.days
          hours = time_diff.seconds // 3600 # get number of hours
          minutes = (time_diff.seconds // 60) % 60 
          seconds=time_diff.seconds
          return {"days":days,"hours":hours,"minutes":minutes,"seconds":seconds}

    def __str__(self):
        return self.offer_name
        
class Orders(models.Model):
    data_added = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    total_price = models.FloatField()
    def total_count(self):
        return sum([item.count for item in self.order_details_set.all()])

class Order_Details(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    count = models.IntegerField()
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
 