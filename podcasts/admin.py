from django.contrib import admin

# Register your models here.
from .models import Episode, NewsItem, Status

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", "title", "pub_date")

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("source_name", "title", "pub_date")

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("state", "description", "date_added")