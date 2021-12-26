from django.urls import path
from .views import *


urlpatterns = [
    path('register/', registerview, name='register'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
    path('activate/<uidb64>/<token>/', activateview, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validateview, name='resetpassword_validate'),
    path('dashboard/', dashboardview, name='dashboard'),
    path('forgotpassword/', forgotpasswordview, name='forgotpassword'),
    path('reset-password/', resetpasswordview, name='reset-password'),
    path('my-orders/', myorderview, name='my_orders'),
    path('edit-profile/', editprofileview, name='edit_profile'),
    path('change-password/', changepasswordview, name='change_password'),
    path('order-detail/<int:order_id>/', orderdetailview, name='order_detail')
]
