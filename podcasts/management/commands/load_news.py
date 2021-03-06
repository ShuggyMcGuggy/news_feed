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
from podcasts.models import Episode, NewsItem, Status

logger = logging.getLogger(__name__)


url_pods = "https://realpython.com/podcasts/rpp/feed"
url_scaled_agile = "http://www.scaledagileframework.com/feed/"
url_101ways = "https://www.101ways.com/feed/"
url_agile_alliance = "https://www.agilealliance.org/feed"
url_leadinagile = "https://www.leadingagile.com/blog/feed/"


l_urls_rss_feeds =['https://www.agilealliance.org/feed',
    'https://blog.gitscrum.com/feed/',
    'https://www.agil8.com/feed/',
    'https://www.scrumexpert.com/feed/'
    ]

def save_new_episodes(feed):
    """Saves new episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

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
    status_new = Status.objects.get(state='New')


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
                status=status_new
            )
            newsitem.save()

# The **** fetch functions to be scheduled for each feed ******
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

# def handle(self, *args, **options):
#     scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#
#     scheduler.add_job(
#         fetch_realpython_episodes,
#         trigger="interval",
#         minutes=2,
#         id="The Real Python Podcast",
#         max_instances=1,
#         replace_existing=True,
#     )
#     logger.info("Added job: The Real Python Podcast.")



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

        scheduler.add_job(
            fetch_scaledagilefrmework_news_items,
            trigger='date',
            id="One off scaled agile",
            max_instances=1,
            replace_existing=True,

        )
        logger.info("Added job: Scaled Agile Framework Feed.")


        scheduler.add_job(
            fetch_101ways_news_items,
            trigger='date',
            id="101 Ways  Feed",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: 101 Ways Feed.")

        scheduler.add_job(
            fetch_agile_alliance_news_items,
            trigger='date',
            id="Agile Alliance Feed",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Agile Alliance Feed.")

        scheduler.add_job(
            fetch_leadinagile_news_items,
            trigger='date',
            id="Lead In Agile feed",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Lead In Agile Feed.")

        # scheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),  # Midnight on Monday, before start of the next work week.
        #     id="Delete Old Job Executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
