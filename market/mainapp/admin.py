from django.contrib import admin
from django.apps import apps
from . models import User,Customers,Basket,Basket_Details,Bill,Bill_details,Category,Product
# Register your models here.
admin.site.register(Customers)
admin.site.register(Basket)
admin.site.register(Basket_Details)
admin.site.register(Bill)
admin.site.register(Bill_details)
admin.site.register(Category)
admin.site.register(Product)

    