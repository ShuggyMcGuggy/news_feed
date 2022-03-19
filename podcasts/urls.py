from django.urls import path
from django.conf.urls import url

from .views import HomePageView, NewsView, PubsView, pub_item
from . import views

urlpatterns = [

    # Home Page
    # path("", HomePageView.as_view(), name="homepage"),
    path("List/", HomePageView.as_view(), name="homepage"),

    # url('', views.home, name='home'),

    # Show all news items
    path('news/', NewsView.as_view(), name='news'),

    # Show all news items and enable page to to saved to static HTML page
    url(r'^news_list_static/$', views.news_list_static, name='news_list_static'),

    # Detail page for a single news item
    url(r'^news_item/(?P<news_item_id>\d+)/$', views.news_item, name='news_item'),
    # path('news_item/((?P<news_item_id>\d+)/$', NewsItemView.as_view(), name='news_item'),

    # Edit page for the News Item
    url(r'^edit_news_item/(?P<news_item_id>\d+)/$', views.edit_news_item, name='edit_news_item'),

    # List of all publications
    url(r'^publications/$', PubsView.as_view(), name='publications'),

    # Detail page for a single publication
    # url(r'^pub_item/(?P<pub_item_id>\d+)/$', pub_item.as_view(), name='pub_item'),
    url(r'^pub_item/(?P<pub_item_id>\d+)/$', views.pub_item, name='pub_item'),

    # Dummy page to load test story
    url(r'test_story/', views.load_test_story, name='load_test_story'),

    # Index page for Real home page (OTHER URLS NEED TO be above this)
    url(r'', views.home, name='home'),
    # path('home/', HomePageView.as_view(), name="homepage"),





]