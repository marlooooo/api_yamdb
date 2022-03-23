from django.contrib import admin

from .models import Title, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

# Register your models here.
