from django.contrib import admin
from product_rating.models import ProductRating


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        ProductRating.objects.select_related('user')
        return super().get_queryset(request).select_related('user')
