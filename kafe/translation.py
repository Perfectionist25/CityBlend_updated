from modeltranslation.translator import TranslationOptions, register
from .models import *

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Food)
class FoodTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
