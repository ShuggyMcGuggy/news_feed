from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

# Register your models here.
# from .models import Episode, NewsItem, Status, Publication, Publication_Stories, PageExport, RSS_feed
from .models import  NewsItem, Status, Publication, Publication_Stories, PageExport, RSS_feed


# @admin.register(Episode)
# class EpisodeAdmin(admin.ModelAdmin):
#     list_display = ("podcast_name", "title", "pub_date")

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "source_name", "title", "pub_date")

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id","state", "description", "date_added")

@admin.register(Publication)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id","title", "description", "date_added")

@admin.register(Publication_Stories)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("publication_id", "news_item_id", "date_added")

@admin.register(PageExport)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_added")

@admin.register(RSS_feed)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "source_name", "is_live")


# class RSS_Feed_Resource(resources.ModelResource):
#    class Meta:
#       model = RSS_feed
#
#
# class RSS_Feed_Admin(ImportExportModelAdmin):
#    resource_class = RSS_Feed_Resource
#
# admin.site.register(RSS_Feed_Resource)



