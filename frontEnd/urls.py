from django.urls import path
from .views import home,login,signup, logout,my_orders, jewelry_list,order_jewelry, order_confirmation, cancel_order

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
    path('my_orders', my_orders, name='my_orders'),
    path('jewelry_list', jewelry_list, name='jewelry_list'),
    path('order_jewelry/<int:jewelry_id>/', order_jewelry, name='order_jewelry'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    ]