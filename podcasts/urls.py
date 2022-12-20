from django.urls import path
from django.conf.urls import url

from .views import HomePageView, NewsView, PubsView,\
    pub_item, NewsNewView, ArticleNewView, ArticleEditView,\
    pub_item_static, ArticleMapStoriesView, ArticleMapStoryLinkNewView, \
    PageExportEditView, page_export

from . import views

urlpatterns = [

    # Home Page
    # path("", HomePageView.as_view(), name="homepage"),
    path("List/", HomePageView.as_view(), name="homepage"),

    # url('', views.home, name='home'),

    # Show all news items
    path('news/', NewsView.as_view(), name='news'),

    # Show list of just new items
    path('news_new/', NewsNewView.as_view(), name='news_new'),

    # Show all news items and enable page to to saved to static HTML page
    url(r'^news_list_static/$', views.news_list_static, name='news_list_static'),

    # Detail page for a single news item
    url(r'^news_item/(?P<news_item_id>\d+)/$', views.news_item, name='news_item'),
    # path('news_item/((?P<news_item_id>\d+)/$', NewsItemView.as_view(), name='news_item'),

    # Edit page for the News Item
    url(r'^edit_news_item/(?P<news_item_id>\d+)/$', views.edit_news_item, name='edit_news_item'),

    # NEWS : Edit page for the News Item with Prev Next & Article link from
    url(r'^edit_news_item_links/(?P<news_item_id>\d+)/$', views.edit_news_item_links, name='edit_news_item_links'),

    # NEWS: Edit page while passing previous and next links
    # This URL is called after the status of the NEws item is change from NEW to another status
    # when the PREVIOUS and NEXT item links cannot be calculated.
    url(r'^edit_news_links_changed/(?P<news_item_id>\d+)/(?P<prev_news_id>\d+)/(?P<next_news_id>\d+)/$', views.edit_news_links_changed, name='edit_news_links_changed'),

    # List of all publications
    url(r'^publications/$', PubsView.as_view(), name='publications'),

    # Detail page for a single publication
    # url(r'^pub_item/(?P<pub_item_id>\d+)/$', pub_item.as_view(), name='pub_item'),
    url(r'^pub_item/(?P<pub_item_id>\d+)/$', pub_item, name='pub_item'),

    # URL to generate a static HTML page for a single publication
    url(r'^pub_item_static/(?P<pub_item_id>\d+)/$', pub_item_static, name='pub_item_static'),

    # Page to create a new Article
    url(r'^article_new/$', ArticleNewView, name='article_new'),

    # Page to Edit an Article
    url(r'^article_edit/(?P<pub_item_id>\d+)/$', ArticleEditView, name='article_edit'),

    # Page to map an Article to stories
    url(r'^article_map_stories/(?P<pub_item_id>\d+)/$', ArticleMapStoriesView, name='article_map_stories'),

    # Page to map an Article to stories
    url(r'^article_map_link/(?P<pub_item_id>(\d+))/(?P<news_item_id>(\d+))/$', ArticleMapStoryLinkNewView, name='article_map_stories_link'),

    # Detail page for a single page export item
    url(r'^page_export/(?P<page_export_id>\d+)/$', views.page_export, name='page_export_item'),

    # Page to view the page export criterion
    url(r'^page_export_edit/(?P<page_export_id>\d+)/$', PageExportEditView,
        name='page_export_edit'),

    # Dummy page to load test story
    url(r'test_story/', views.load_test_story, name='load_test_story'),

    # Index page for Real home page (OTHER URLS NEED TO be above this)
    url(r'', views.home, name='home'),
    # path('home/', HomePageView.as_view(), name="homepage"),





]