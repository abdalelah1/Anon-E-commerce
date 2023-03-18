from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customers(models.Model):
        customer_name = models.CharField(max_length=30,unique=True)
        customer_Birth_date = models.CharField(max_length=30)
        customer_Mobile_number=models.CharField(max_length=15)
        customer_gender=models.CharField(max_length=4)
        customer_email=models.CharField(max_length=255)
        custome_fk=models.OneToOneField(User,on_delete=models.CASCADE,null=False)
        def __str__(self) :
                return str(self.id)
class Category(models.Model):
        Category_name=models.CharField(max_length=100)
        Category_totoal_count=models.IntegerField(default=0)
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
        def __str__(self) :
                return str(self.id)
class Product_Rating(models.Model):
        rating_stars=models.IntegerField()
        rating_description=models.CharField(max_length=100)
        product_rating_product_fk=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
        product_rating_customer_fk=models.ForeignKey(Customers,on_delete=models.CASCADE,null=False)
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
        bill_datails_vat=models.FloatField()
        bill_datails_final_price=models.FloatField()
        bill_details_counter=models.IntegerField()
        bill_details_date=models.CharField(max_length=255)
        bill_details_bill_fk=models.ForeignKey(Bill,on_delete=models.CASCADE)
        def __str__(self) :
                return self.id 




        

