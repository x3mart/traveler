from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode
import os

# Create your models here.
def lang_icon_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'langicon/{0}/{1}{2}'.format(slugify(unidecode(instance.name)), slugify(unidecode(name)), extension)


class Language(models.Model):
    name = models.CharField(_('Название'), max_length=25)
    short_name = models.CharField(_('Краткое_название'), max_length=25)
    icon = models.ImageField(_('Иконка'), max_length=255, upload_to=lang_icon_path)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Язык')
        verbose_name_plural = _('Языки')