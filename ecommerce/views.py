from django.shortcuts import render
from store.models import Product, Featured, SpecialOffer, BannerSlide
from django.core.paginator import *


def homeview(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    special_offer = SpecialOffer.objects.all().order_by('-date_added')[:1]
    banner_slide = BannerSlide.objects.all().order_by('-date_added')[:3]
    featured_products = Featured.objects.all().filter(product__is_available=True).order_by('-date_added')[:8]
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products': paged_products,
        'featured_products': featured_products,
        'special_offer': special_offer,
        'banner_slide': banner_slide
    }
    return render(request, 'home.html', context)

