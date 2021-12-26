from django.db import models
from django.shortcuts import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=150)
    cat_slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='photos/category', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('product_by_category', args=[self.cat_slug])

    def __str__(self):
        return self.category_name
