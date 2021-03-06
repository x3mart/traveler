from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Referral(models.Model):
    score = models.PositiveSmallIntegerField(_('Реферальные быллы'), null=True, blank=True)
    referral = models.OneToOneField(('accounts.User'), on_delete=models.PROTECT, related_name='referral')
    beneficiary = models.ForeignKey(('accounts.User'), on_delete=models.PROTECT, related_name='beneficiary_referrals')
    tour = models.ForeignKey(('tours.Tour'), on_delete=models.PROTECT, related_name='tour_referrals', null=True, blank=True)

    class Meta:
        verbose_name = _('Реферал')
        verbose_name_plural = _('Рефералы')
