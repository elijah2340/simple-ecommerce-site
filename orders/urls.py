from django.urls import path
from .views import *

urlpatterns = [
    path('place_order/', placeorderview, name='place_order'),
    path('paymentsuccessful/<int:id>/', paymentview, name='payments'),
    path('place_order/<int:id>/', apply_coupon, name='apply_coupon'),

]
