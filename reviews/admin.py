from django.contrib import admin

from reviews.models import ExpertReview, TourReview

# Register your models here.
admin.site.register(TourReview)
admin.site.register(ExpertReview)