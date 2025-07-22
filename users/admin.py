from django.contrib import admin
from .models import *


@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    ...