from django.urls import path
from . import views

app_name = 'kafe'

urlpatterns = [
    path('', views.home, name='home'),
    path('foods/', views.foods_list, name='foods'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart_item/<int:pk>/', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart_item/<int:pk>/', views.edit_cart_item, name='edit_cart_item'),
    path('food_detail/<int:pk>/', views.food_detail, name='food_detail'),
    path('cart/create_order/', views.create_order, name='create_order'),
    path('orders/', views.orders, name='orders'),
    path('helper/', views.helper, name='helper'),
    path('info_order/', views.info_order, name='info_order'),
    path('discounted_foods/', views.discounted_foods, name='discounted_foods'),
]
