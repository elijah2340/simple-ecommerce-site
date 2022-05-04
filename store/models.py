from django.db import models
from django.db.models import Avg, Count

from category.models import Category
from django.shortcuts import reverse
from accounts.models import Account, UserProfile


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(max_length=100000, blank=True)
    product_specifications = models.TextField(blank=True)
    key_spec1 = models.CharField(max_length=1000, blank=True)
    key_spec2 = models.CharField(max_length=1000, blank=True)
    key_spec3 = models.CharField(max_length=1000, blank=True)
    key_spec4 = models.CharField(max_length=1000, blank=True)
    price = models.IntegerField()
    image = models.ImageField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.cat_slug, self.slug])

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


choice = (
    ('color', 'color'),
    ('size', 'size')
)


class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    variation_category = models.CharField(max_length=255, choices=choice)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.variation_value

    objects = VariationManager()


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.user.first_name} - {self.subject}'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'prooductgallery'
        verbose_name_plural = 'product gallery'


class Featured(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name


class SpecialOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name


class BannerSlide(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name