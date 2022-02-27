from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

# Create your models here.
class TourReview(models.Model):
    tour = models.ForeignKey('tours.TourBasic', on_delete=models.CASCADE, verbose_name=_('Тур'), related_name='tour_reviews', null=True, blank=True)
    body = RichTextField(_('Отзыв'))
    rating = models.DecimalField(_('Оценка'), max_digits=2, decimal_places=1)
    author = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE, verbose_name=_('Путешественник'), related_name='customer_tours_reviews')

    def __str__(self):
        return f'{self.tour.name} {self.author.full_name}'
    
    class Meta:
        verbose_name = _('Отзыв о туре')
        verbose_name_plural = _('Отзывы о турах')


class ExpertReview(models.Model):
    expert = models.ForeignKey('accounts.Expert', on_delete=models.CASCADE, verbose_name=_('Тур'), related_name='expert_reviews')
    body = RichTextField(_('Отзыв'))
    rating = models.DecimalField(_('Оценка'), max_digits=2, decimal_places=1)
    author = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE, verbose_name=_('Тур'), related_name='customer_experts_reviews')

    def __str__(self):
        return f'{self.expert.full_name} {self.author.full_name}'
    
    class Meta:
        verbose_name = _('Отзыв об эксперте')
        verbose_name_plural = _('Отзывы об экспертах')