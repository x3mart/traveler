from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

# Create your models here.
class LegalDocument(models.Model):
    docs_name = models.CharField(_('Название'), max_length=255,  null=True, blank=True,)
    docs_slug = models.CharField(_('slug'), max_length=255,  null=True, blank=True,)
    docs_title = models.CharField(_('Заголовок'), max_length=255,  null=True, blank=True,)
    docs_subtitle = models.CharField(_('Подзаголовок'), max_length=255,  null=True, blank=True,)
    docs_meta_tag = models.TextField(_('Мета теги'), max_length=255,  null=True, blank=True,)
    docs_body = RichTextField(_('Текст'), null=True, blank=True,)

    class Meta:
        verbose_name = _('Юр документ')
        verbose_name_plural = _('Юр документы')
        ordering = ['docs_name']


    def __str__(self):
        return self.docs_name if self.docs_name else '--'