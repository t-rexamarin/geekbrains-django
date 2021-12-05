from django.contrib import admin
from .models import Product, ProductCategory

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class Product(admin.ModelAdmin):

    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'category')
    readonly_fields = ('description',)
    ordering = ('name', 'price',)
    search_fields = ('name',)
