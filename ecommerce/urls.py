from django.contrib import admin
from django.urls import path, include
from .views import homeview
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
admin.site.site_header = "Eli-Ecommerce Admin"
admin.site.site_title = "Eli=Ecommerce Admin Panel"
admin.site.index_title = "Welcome to Elijah Admin Panel"

urlpatterns = [
    path('elijahlogin/', admin.site.urls),
    path('home', homeview, name='home'),
    path('', RedirectView.as_view(url='/home')),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('account/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
