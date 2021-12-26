from django.urls import path
from .views import *


urlpatterns = [
    path('', storeview, name='store'),
    path('category/<slug:cat_slug>/', storeview, name='product_by_category'),
    path('category/<slug:cat_slug>/<slug:slug>/', productDetail, name='product_detail'),
    path('search', searchview, name='search'),
    path('submit_review/<int:product_id>/', reviewview, name='review')
]
