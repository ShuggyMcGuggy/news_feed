from django.test import TestCase
from django.utils import timezone
from .models import Episode, NewsItem, Status, RSS_feed
from django.urls.base import reverse
from datetime import datetime
import requests
from .management.commands.startjobs import fetch_leadinagile_news_items


# Create your tests here.


# class PodCastsTests(TestCase):
#     def setUp(self):
#         self.episode = Episode.objects.create(
#             title="My Awesome Podcast Episode",
#             description="Look mom, I made it!",
#             pub_date=timezone.now(),
#             link="https://myawesomeshow.com",
#             image="https://image.myawesomeshow.com",
#             podcast_name="My Python Podcast",
#             guid="de194720-7b4c-49e2-a05f-432436d3fetr",
#         )
#
#     def test_episode_content(self):
#         self.assertEqual(self.episode.description, "Look mom, I made it!")
#         self.assertEqual(self.episode.link, "https://myawesomeshow.com")
#         self.assertEqual(
#             self.episode.guid, "de194720-7b4c-49e2-a05f-432436d3fetr"
#         )
#
#     def test_episode_str_representation(self):
#         self.assertEqual(
#             str(self.episode), "My Python Podcast: My Awesome Podcast Episode"
#         )

    # def test_home_page_status_code(self):
    #     response = self.client.get("/")
    #     self.assertEqual(response.status_code, 200)

    # def test_home_page_uses_correct_template(self):
    #     response = self.client.get(reverse("homepage"))
    #     self.assertTemplateUsed(response, "homepage.html")
    #
    # def test_homepage_list_contents(self):
    #     response = self.client.get(reverse("homepage"))
    #     self.assertContains(response, "My Awesome Podcast Episode")

class News_gather(TestCase):
    fixtures = ["./test/test_fixtures/status.json",
                "./test/test_fixtures/newsitem.json",
                "./test/test_fixtures/rss_feeds.json"
                ]
    def setUp(self):
            self.news_item = NewsItem.objects.create(
                source_name="Test Source",
            title = "My Title",
            description = "My Description",
            pub_date = datetime.now(),
            link = "https://pling.com",
            image = "https://image.com",
            podcast_name = "podcast name",
            guid = "1",
            comment = "My Comment",
            status = Status.objects.last(),
            star_rating = 5
            )

    def test_should_create_status_list(self):
        len_status = len(Status.objects.all())
        self.assertEqual(len_status, 4, "Status Table incorrect number of entries")

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


    def test_kwargs_filter_news(self):
        len_news = len(NewsItem.objects.all())
        print("the number of news item: " + str(len_news))
        self.assertNotEqual(len_news, 0, "The list is empty")
        kwargs = {"source_name": "The Low-code daily"}
        l_newsitems = NewsItem.objects.filter(**kwargs)
        print(l_newsitems)

    def test_urls_edit_news_links_changed(self):
        response = self.client.get("/edit_news_links_changed/2476/2476/1")
        self.assertEqual(response.status_code, 200)
        result = ''
        try:
            result = reverse('podcasts:edit_news_links_changed',
                args=['2476', '2476', '2476'])
        except:
            self.assertNotEqual(result, '', "The URL did not resolve")
        finally:
            self.assertEqual(result,"/edit_news_links_changed/2476/2476/2476/", "URL does not match" )

    def test_urls_edit_news_links_filtered(self):
        result = ''
        try:
            result = reverse('podcasts:edit_news_links_filtered',
                args=['2476', '2476', '2476','1'])
        except:
            self.assertNotEqual(result, '', "The URL did not resolve")
        finally:
            self.assertEqual(result,"/edit_news_links_filtered/2476/2476/2476/1/", "URL does not match" )

        response = self.client.get("/edit_news_links_filtered/2476/2476/2476/1/")
        self.assertEqual(response.status_code, 200, "Client test page not correctly found")
        my_response = requests.get(" http://127.0.0.1:8000/edit_news_links_filtered/2476/2475/2477/1/")
        self.assertEqual(response.status_code, 200, "HTTP request Page not correctly found")
    def test_filter_by_sourcename(self):
        # Get the ID of the NEW Status record
        status_new = Status.objects.filter(state='New')
        # Get the rss_feed object for Not Filtered
        rss_source = RSS_feed.objects.get(id='1')
        for rss_source in RSS_feed.objects.all():
            l_news_items = NewsItem.objects.filter(status=status_new[0].id, source_name=rss_source.source_name).order_by( "-pub_date")
            print("Number of news items for source: " + rss_source.source_name + " is: " + str(len(l_news_items)))






