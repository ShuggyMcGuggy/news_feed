# ********  Standard Library ********
import logging

# *********  Django ********
from django.conf import settings
from django.core.management.base import BaseCommand

# *******   Third Party ********
# import dateutil.utils
import feedparser
import requests
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
# import datetime

# ******* Models **********
from podcasts.models import Episode, NewsItem

logger = logging.getLogger(__name__)


url_pods = "https://realpython.com/podcasts/rpp/feed"
url_scaled_agile = "http://www.scaledagileframework.com/feed/"
url_101ways = "https://www.101ways.com/feed/"
url_agile_alliance = "https://www.agilealliance.org/feed"
url_leadinagile = "https://www.leadingagile.com/blog/feed/"
url_ESG_News = "https://www.esgtoday.com/feed/"


l_urls_rss_feeds =['https://www.agilealliance.org/feed',
    'https://blog.gitscrum.com/feed/',
    'https://www.agil8.com/feed/',
    'https://www.scrumexpert.com/feed/'
    ]
# ------------------------------------------
''' This section cover the environment vairables to control data feeds
Using Boolean flags to control which of the feeds is live
'''

b_scaled_agile_framework = True
b_101ways = True
b_agile_alliance = True
b_leadinagile_news = True
b_ESG_News = True

int_mins = 4


# For testing, the method for recovery is to just delete the last few entries in the database and then re-run
# One option might be to use a test database and provide functions to clear this down afterwards.


#--------------


def save_new_episodes(feed):
    """Saves new episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]
    #podcast_image = "https://frozen-brushlands-72168.herokuapp.com/staticfiles/imgs/agile_pm.png"

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title=item.title,
                description=item.description,
                #pub_date=parser.parse(item.published),
                pub_date=item.published_parsed,
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()
# *** Functions to load news feed *****
def save_new_news_items(feed):
    """Saves new news items to the database.

    Checks the news_item GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    source_title = feed.channel.title
    # podcast_image = feed.channel.image["https://frozen-brushlands-72168.herokuapp.com/staticfiles/imgs/agile_pm.png"]
    podcast_image = "https://frozen-brushlands-72168.herokuapp.com/staticfiles/imgs/agile_pm.png"

    for item in feed.entries:
        if not NewsItem.objects.filter(guid=item.guid).exists():
            newsitem = NewsItem(
                source_name= source_title,
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                guid=item.guid,
            )
            newsitem.save()

# The **** fetch functions to be scheduled for each feed ******

def fetch_ESG_News_episodes():
    """Fetches new episodes from RSS for The Real Python Podcast."""
    _feed = feedparser.parse(requests.get(url_ESG_News, headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_news_items(_feed)

def fetch_realpython_episodes():
    """Fetches new episodes from RSS for The Real Python Podcast."""
    _feed = feedparser.parse(requests.get("https://realpython.com/podcasts/rpp/feed", headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_episodes(_feed)


def fetch_talkpython_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse(requests.get("https://talkpython.fm/episodes/rss", headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_episodes(_feed)

def fetch_scaledagilefrmework_news_items():
    """Fetches new episodes from RSS for the Scale Agile Framework RSS feed"""
    _feed = feedparser.parse(requests.get(url_scaled_agile, headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_news_items(_feed)

def fetch_101ways_news_items():
    """Fetches new episodes from RSS for the 101 Ways RSS feed"""
    _feed = feedparser.parse(requests.get(url_101ways, headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_news_items(_feed)

def fetch_agile_alliance_news_items():
    """Fetches new episodes from RSS for the 101 Ways RSS feed"""
    _feed = feedparser.parse(requests.get(url_agile_alliance, headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_news_items(_feed)

def fetch_leadinagile_news_items():
    """Fetches new episodes from RSS for the 101 Ways RSS feed"""
    _feed = feedparser.parse(requests.get(url_leadinagile , headers={'User-Agent': 'Mozilla/5.0'}).content)
    save_new_news_items(_feed)
    return True

def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        fetch_realpython_episodes,
        trigger="interval",
        minutes= int_mins,
        id="The Real Python Podcast",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job: The Real Python Podcast.")



# ***********************  Set up command functino call *****
class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")



        # scheduler.add_job(
        #     fetch_realpython_episodes,
        #     trigger="interval",
        #     minutes=60,
        #     id="The Real Python Podcast",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added job: The Real Python Podcast.")
        #
        # scheduler.add_job(
        #     fetch_talkpython_episodes,
        #     trigger="interval",
        #     minutes=60,
        #     id="Talk Python Feed",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added job: Talk Python Feed.")

        if b_ESG_News == True:
            scheduler.add_job(
                fetch_ESG_News_episodes,
                trigger="interval",
                #date=2,
                minutes=int_mins,
                id="ESG News Feed",
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job: ESG News Feed.")

        if b_scaled_agile_framework == True:
            scheduler.add_job(
                fetch_scaledagilefrmework_news_items,
                trigger="interval",
                #date=2,
                minutes=int_mins,
                id="Scaled Agile Framework Feed",
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job: Scaled Agile Framework Feed.")

        if b_101ways == True:
            scheduler.add_job(
                fetch_101ways_news_items,
                trigger="interval",
                minutes=int_mins,
                id="101 Ways  Feed",
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job: 101 Ways Feed.")

        if b_agile_alliance == True:
            scheduler.add_job(
                fetch_agile_alliance_news_items,
                trigger="interval",
                minutes=int_mins,
                id="Agile Alliance Feed",
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job: Agile Alliance Feed.")

        if b_leadinagile_news == True:
            scheduler.add_job(
                fetch_leadinagile_news_items,
                trigger="interval",
                minutes=int_mins,
                id="Lead In Agile feed",
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job: Lead In Agile Feed.")



            scheduler.add_job(
                delete_old_job_executions,
                trigger=CronTrigger(
                day_of_week="mon",
                hour="00",
                minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")



# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         feed = feedparser.parse(requests.get(url_pods, headers={'User-Agent': 'Mozilla/5.0'}).content)
#         podcast_title = feed.channel.title
#         podcast_image = feed.channel.image["href"]
#         # feed = feedparser.parse(requests.get("https://realpython.com/podcasts/rpp/feed", headers={'User-Agent': 'Mozilla/5.0'}).content)
#         # podcast_title = feed.channel.title
#         # podcast_image = feed.channel.image["href"]
#         # podcast_title = "google Search"
#         # podcast_image = "https://files.realpython.com/media/real-python-logo-square.28474fda9228.png",
#
#         for item in feed.entries:
#             # if not Episode.objects.filter(guid=item.guid).exists():
#             episode = Episode(
#                 title=item.title,
#                 description=item.description,
#                 pub_date=parser.parse(item.published),
#                 link=item.link,
#                 image=podcast_image,
#                 podcast_name=podcast_title,
#                 guid=item.guid,
#             )
#             episode.save()

        # item = "https://pegasusprint214.com/2021/11/30/the-iias-agile-risk-management-my-thoughts/"
        #
        # episode = Episode(
        #         title="link to: " + item,
        #         description="description",
        #         pub_date=dateutil.utils.today(),
        #         link=item,
        #         image=podcast_image,
        #         podcast_name=podcast_title,
        #         guid='a123'
        #     )
        # episode.save()

        # for item in feed_links:
        #     episode = Episode(
        #         title="link to: " + item,
        #         description="description",
        #         pub_date=dateutil.utils.today(),
        #         link=item,
        #         image=podcast_image,
        #         podcast_name=podcast_title,
        #         guid='a123'
        #     )
        #     episode.save()