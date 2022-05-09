from django.db import models
from account.models import MyUser
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Category')
    slug = models.CharField(max_length=50, primary_key=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Shop(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Author',
                               related_name='shops')
    name = models.CharField(max_length=50, unique=True, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(upload_to='media/shop_images', blank=True, null=True,
                              verbose_name='Image')
    address = models.TextField(verbose_name='Address')

    def __str__(self):
        return self.name

class Product(models.Model):
    CHOICES = (('in stock', 'in stock'),('out of stock', 'out of stock'))
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='products',
                               related_name='products')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products',
                             verbose_name='Shop')
    name = models.CharField(max_length=255, unique=False, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='shops',
                                 verbose_name='Category')
    status = models.CharField(max_length=50, choices=CHOICES)
    image = models.ImageField(upload_to='media/product_images', verbose_name='Image')
    price = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return f'{self.shop}: {self.name}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class RatingStar(models.Model):
    value = models.SmallIntegerField(primary_key=True, unique=True, default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating star"
        verbose_name_plural = "Rating stars"

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.product} - {self.star}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

class Saved(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='saved')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved')

    def __str__(self):
        return f'{self.author} - {self.product}'