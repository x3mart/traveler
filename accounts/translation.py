from modeltranslation.translator import register, TranslationOptions
from .models import Customer, Expert, User


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name',)
    # required_languages = {'en': ('first_name', 'last_name',), 'ru': ('last_name',)}


@register(Expert)
class ExpertTranslationOptions(TranslationOptions):
    fields = ('country', 'city', 'visited_countries', 'about')


@register(Customer)
class CustomerTranslationOptions(TranslationOptions):
    pass