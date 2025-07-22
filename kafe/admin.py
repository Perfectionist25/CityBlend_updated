from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from .models import *

@admin.register(Food)
class ProductAdmin(TranslationAdmin):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    list_display = ('title', 'price', 'is_new', 'is_discounted','category')
    search_fields = ('title', 'price')
    list_filter = ('is_new', 'is_discounted')
    prepopulated_fields = {"slug": ('title',)}

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ...
