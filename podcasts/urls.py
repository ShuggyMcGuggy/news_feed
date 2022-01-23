from django.urls import path
from django.conf.urls import url

from .views import HomePageView, NewsView
from . import views

urlpatterns = [

    # Home Page
    path("", HomePageView.as_view(), name="homepage"),

    # Show all news items
    path('news/', NewsView.as_view(), name='news'),

    # Show all news items and enable page to to saved to static HTML page
    # url(r'^news_list_static/$', views.news_list_static, name='news_list_static'),

    # Detail page for a single news item
    url(r'^news_item/(?P<news_item_id>\d+)/$', views.news_item, name='news_item'),
    # path('news_item/((?P<news_item_id>\d+)/$', NewsItemView.as_view(), name='news_item'),

    # Edit page for the News Item
    url(r'^edit_news_item/(?P<news_item_id>\d+)/$', views.edit_news_item, name='edit_news_item'),



]