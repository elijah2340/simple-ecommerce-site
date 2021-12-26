from django.contrib import admin
from django.urls import path, include
from .views import homeview
from django.conf.urls.static import static
from django.conf import settings
admin.site.site_header = "Eli-Ecommerce Admin"
admin.site.site_title = "Eli=Ecommerce Admin Panel"
admin.site.index_title = "Welcome to Elijah Admin Panel"

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('elijahlogin/', admin.site.urls),
    path('', homeview, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('account/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
