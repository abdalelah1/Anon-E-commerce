from django.urls import path
from . import views

urlpatterns=[
       # path('login/',views.login,name='log in ')
       path('',views.store,name='store'),
       path('login_Signup/',views.loginpage,name='login_Signup'),
       path('searchProduct',views.SearchProduct,name='searchProduct'),
       path('register/',views.RegisterUser,name='register'),
       path('basket/',views.basket,name='basket'),
       path('update_item/',views.updateItem, name="update"),
       path('details/<int:product_id>/', views.view_item, name='details'),


]
