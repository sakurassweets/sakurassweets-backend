from rest_framework import viewsets
from .serializers import RatingListSerializer

from .models import ProductRating


"""
For future development # NOQA
"""
# def update_rating(product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     ratings = ProductRating.objects.filter(product=product)
#     avg_product_rating = ratings.aggregate(Avg("rating"))['rating__avg']  # Calculate average rating
#     product.rating = avg_product_rating if avg_product_rating is not None else 0  # Set average rating
#     product.save()  # Save the updated product rating


class RatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.select_related('product').prefetch_related('user')
    serializer_class = RatingListSerializer

