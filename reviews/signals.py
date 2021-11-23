from django.db.models.aggregates import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ExpertReview, TourReview


@receiver(post_save, sender=ExpertReview)
def expert_review_post_save(instance, **kwargs):
    expert = instance.expert
    expert.rating = expert.aggregate(avg=Avg('expert_reviews__rating'))['avg']
    expert.save()

@receiver(post_save, sender=TourReview)
def expert_review_post_save(instance, **kwargs):
    expert = instance.tour.expert
    expert.tours_rating = expert.aggregate(avg=Avg('tours__tour_reviews__rating'))['avg']
    expert.save()
