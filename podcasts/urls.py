from django.urls import path
from django.conf.urls import url

from .views import HomePageView, NewsView
from . import views

urlpatterns = [

    # Home Page
    path("", HomePageView.as_view(), name="homepage"),

    # Show all news items
    path('news/', NewsView.as_view(), name='news'),

    # Detail page for a single news item
    url(r'^news_item/(?P<news_item_id>\d+)/$', views.news_item, name='news_item'),
    # path('news_item/((?P<news_item_id>\d+)/$', NewsItemView.as_view(), name='news_item'),

]