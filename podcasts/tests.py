from django.test import TestCase
from django.utils import timezone
from .models import Episode, NewsItem, Status
from django.urls.base import reverse
from datetime import datetime

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
                "./test/test_fixtures/newsitem.json"
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


