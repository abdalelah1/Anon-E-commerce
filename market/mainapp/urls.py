from django.urls import path,include
from . import views

urlpatterns=[
       # path('login/',views.login,name='log in ')
       path('checkout/',views.checkout,name='checkout'),
       path('logout/', views.logout_view, name='logout'),
       path('',views.main_page,name='main_page'),
       path('mainProduct/',views.mainPorduct,name='mainProduct'),
       path('old/',views.store,name="store"),
       path('login_Signup/',views.loginpage,name='login_Signup'),
       path('searchProduct',views.SearchProduct,name='searchProduct'),
       path('register/',views.RegisterUser,name='register'),
       path('basket/',views.basket,name='basket'),
       path('update_item/',views.updateItem, name="update"),
       path('home/',views.home, name="home"),
       path('order_details/',views.order_details, name="order_details"),
       path('orderHistory/',views.order_history, name="orderHistory"),
       path('details/<int:product_id>/', views.view_item, name='details'),
       path('order_details/<int:orderID>/', views.order_details, name='order_details'),
       path('login/',views.log_in ,name='login'),
       path('register_customer/',views.register_customer,name='register_customer'),
       path('category/<int:category_id>/', views.show_category_products, name='category_products')


]
