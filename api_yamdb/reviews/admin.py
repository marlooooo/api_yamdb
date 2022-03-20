from django.contrib import admin

from .models import Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass

# Register your models here.
