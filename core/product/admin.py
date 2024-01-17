from django.contrib import admin
from product.models import Product, ProductType, PriceCurrency

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(PriceCurrency)
