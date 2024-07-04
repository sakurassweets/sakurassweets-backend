from rest_framework import viewsets
from .serializers import ReviewListSerializer
from components.review import permissions as custom_permissions

from .models import ProductReview


"""
For future development # NOQA
"""
# def update_rating(product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     ratings = ProductRating.objects.filter(product=product)
#     avg_product_rating = ratings.aggregate(Avg("rating"))['rating__avg']  # Calculate average rating
#     product.rating = avg_product_rating if avg_product_rating is not None else 0  # Set average rating
#     product.save()  # Save the updated product rating


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.select_related('product').prefetch_related('user')
    serializer_class = ReviewListSerializer
    permission_classes = [custom_permissions.IsReviewOwnerOrStaff]

