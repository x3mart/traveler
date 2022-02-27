from django.db.models import Avg, Count
from django.dispatch import receiver
from django.db.models.signals import post_save

from tours.models import Tour, TourBasic
from .models import ExpertReview, TourReview
from accounts.models import Expert


@receiver(post_save, sender=ExpertReview)
def expert_review_post_save(instance, **kwargs):
    expert = instance.expert
    expert.rating = Expert.objects.filter(pk=expert.id).aggregate(avg=Avg('expert_reviews__rating'))['avg']
    expert.reviews_count = Expert.objects.filter(pk=expert.id).aggregate(count=Count('expert_reviews'))['count']
    expert.save()

@receiver(post_save, sender=TourReview)
def tour_review_post_save(instance, **kwargs):
    tour = instance.tour
    tour.rating = TourBasic.objects.filter(pk=tour.id).aggregate(avg=Avg('tour_reviews__rating'))['avg']
    tour.reviews_count = TourBasic.objects.filter(pk=tour.id).aggregate(count=Count('tour_reviews'))['count']
    tour.save()
    expert = instance.tour.expert
    expert.tours_rating = Expert.objects.filter(pk=expert.id).aggregate(avg=Avg('tours__rating'))['avg']
    expert.tour_reviews_count = Expert.objects.filter(pk=expert.id).aggregate(count=Count('tours__tour_reviews'))['count']
    expert.save()
