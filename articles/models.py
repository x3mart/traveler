from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import default, slugify
from unidecode import unidecode
import os
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
def article_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'tourtypes/{0}/{1}{2}'.format(slugify(unidecode(instance.title)), slugify(unidecode(name)), extension)


class BaseAbstractArticle(models.Model):
    title = models.CharField(_('Заголовок'), max_length=150)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    image = models.ImageField(_('Главное фото'), max_length=255, upload_to=article_path, null=True, blank=True)
    text = RichTextUploadingField(_('Текст'))
    date = models.DateField(_('Дата публикации'), null=True, blank=True)
    reading_time = models.PositiveIntegerField(_('Время чтения'), null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta():
        abstract = True
    
    def __str__(self):
        return self.title


class Article(BaseAbstractArticle):
    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')


class Blog(BaseAbstractArticle):
    author = models.ForeignKey('accounts.User', verbose_name=_('Автор'), on_delete=models.CASCADE, related_name='blogs')
    class Meta:
        verbose_name = _('Блог')
        verbose_name_plural = _('Блоги')