from rest_framework import viewsets, mixins

from reviews.models import TourReview
from reviews.serializers import TourReviewSerializer

# Create your views here.
class TourReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    queryset = TourReview.objects.all()
    serializer_class = TourReviewSerializer
 