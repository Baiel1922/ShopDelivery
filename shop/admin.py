from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    search_fields = ['name', ]

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ['name', ]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'shop']
    list_filter = ('category', )

class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'star', 'author')
    list_display_links = ('id', 'product')
    search_fields = ['product', 'author']
    list_filter = ('star', )

class SavedAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'product')
    list_display_links = ('id', 'author', 'product')
    search_fields = ['author', 'product']

admin.site.register(RatingStar)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Saved, SavedAdmin)
admin.site.register(Rating, RatingAdmin)