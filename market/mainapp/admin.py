from django.contrib import admin
from django.apps import apps
from . models import User,Customers,Basket,Basket_Details,Bill,Bill_details,Category,Product,Offer,ShippingInfo,Order_Details,Orders
# Register your models here.
admin.site.register(Customers)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Basket)
admin.site.register(Basket_Details)
admin.site.register(Offer)
admin.site.register(ShippingInfo)
admin.site.register(Orders)
admin.site.register(Order_Details)
    