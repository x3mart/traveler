from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

# Create your models here.
class LegalDocument(models.Model):
    docs_title = models.CharField(_('Заголовок'), max_length=255,  null=True, blank=True,)
    docs_subtitle = models.CharField(_('Подзаголовок'), max_length=255,  null=True, blank=True,)
    docs_meta_tag = models.TextField(_('Мета теги'), max_length=255,  null=True, blank=True,)
    docs_body = RichTextField(_('Текст'), max_length=255,  null=True, blank=True,)