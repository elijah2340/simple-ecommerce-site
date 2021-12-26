from django.urls import path
from .views import *

urlpatterns = [
    path('', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('remove-item/<int:product_id>/<int:cart_item_id>/', remove_item, name='remove_item'),
    path('checkout/', checkoutview, name='checkout')


]
