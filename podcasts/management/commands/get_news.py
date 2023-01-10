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

from src.gmail import *

# import datetime

# ******* Models **********
from podcasts.models import Episode, NewsItem, Status, RSS_feed

logger = logging.getLogger(__name__)


url_pods = "https://realpython.com/podcasts/rpp/feed"
url_scaled_agile = "http://www.scaledagileframework.com/feed/"
url_101ways = "https://www.101ways.com/feed/"
url_agile_alliance = "https://www.agilealliance.org/feed"
url_leadinagile = "https://www.leadingagile.com/blog/feed/"
url_ESG_News = "https://esgnews.com/feed/"
url_esg_today = "https://www.esgtoday.com/feed/"


l_urls_rss_feeds =['https://www.agilealliance.org/feed',
    'https://blog.gitscrum.com/feed/',
    'https://www.agil8.com/feed/',
    'https://www.scrumexpert.com/feed/'
    ]
# ------------------------------------------
''' This section cover the environment vairables to control data feeds
Using Boolean flags to control which of the feeds is live
'''
b_bulk = True
b_scaled_agile_framework = b_bulk
b_101ways = b_bulk
b_agile_alliance = b_bulk
b_leadinagile_news = b_bulk
b_esg_today = b_bulk

b_ESG_News = True

int_mins = 4


# For testing, the method for recovery is to just delete the last few entries in the database and then re-run
# One option might be to use a test database and provide functions to clear this down afterwards.


#--------------

# **** Function to read all the RSS Feed entries from the RSS_Feed Table
def collect_live_rss_feeds():
    body_text = "Data Feeds Executed: \n\n"
    for rss_item in RSS_feed.objects.filter(is_live=True):
        """Fetches new episodes from RSS for the live feeds"""
        try:
            _feed = feedparser.parse(requests.get(rss_item.feed_url, headers={'User-Agent': 'Mozilla/5.0'}).content)
            _feed.channel.image = rss_item.image_url
            save_new_news_items(_feed)
            body_text = body_text + "\tRan job: fetch: " + rss_item.source_name + "\n"
            logger.info("Ran job: fetch: " + rss_item.source_name)
        except:
            body_text = body_text + "\tRan job: fetch: " + rss_item.source_name + "\n"
            logger.info("JOB FAILED: fetch: " + rss_item.source_name)
    return body_text




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
    # podcast_image = "https://frozen-brushlands-72168.herokuapp.com/staticfiles/imgs/agile_pm.png"
    # podcast_image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
    podcast_image = feed.channel.image
    status_new = Status.objects.filter(state='New')


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
                status=status_new[0],
            )
            newsitem.save()

# The **** fetch functions to be scheduled for each feed ******

# def fetch_ESG_News_episodes():
#     """Fetches new episodes from RSS for The Real Python Podcast."""
#     _feed = feedparser.parse(requests.get(url_ESG_News, headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_news_items(_feed)
#
# def fetch_esg_today_episodes():
#     """Fetches new episodes from RSS for The Real Python Podcast."""
#     _feed = feedparser.parse(requests.get(url_esg_today, headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/ESGToday.png"
#     save_new_news_items(_feed)
#
# def fetch_realpython_episodes():
#     """Fetches new episodes from RSS for The Real Python Podcast."""
#     _feed = feedparser.parse(requests.get("https://realpython.com/podcasts/rpp/feed", headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_episodes(_feed)
#
#
# def fetch_talkpython_episodes():
#     """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
#     _feed = feedparser.parse(requests.get("https://talkpython.fm/episodes/rss", headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_episodes(_feed)
#
# def fetch_scaledagilefrmework_news_items():
#     """Fetches new episodes from RSS for the Scale Agile Framework RSS feed"""
#     _feed = feedparser.parse(requests.get(url_scaled_agile, headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_news_items(_feed)
#
# def fetch_101ways_news_items():
#     """Fetches new episodes from RSS for the 101 Ways RSS feed"""
#     _feed = feedparser.parse(requests.get(url_101ways, headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_news_items(_feed)
#
# def fetch_agile_alliance_news_items():
#     """Fetches new episodes from RSS for the 101 Ways RSS feed"""
#     _feed = feedparser.parse(requests.get(url_agile_alliance, headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_news_items(_feed)
#
# def fetch_leadinagile_news_items():
#     """Fetches new episodes from RSS for the 101 Ways RSS feed"""
#     _feed = feedparser.parse(requests.get(url_leadinagile , headers={'User-Agent': 'Mozilla/5.0'}).content)
#     _feed.channel.image = "https://frozen-brushlands-72168.herokuapp.com/static/imgs/agile_pm.png"
#     save_new_news_items(_feed)
#     return True

def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)





# ***********************  Set up command function call *****
class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        # scheduler.add_jobstore(DjangoJobStore(), "default")
        # try:
        #     fetch_ESG_News_episodes()
        #     logger.info("Ran job: fetch ESG News Feed.")
        # except:
        #     logger.info("job FAILED: fetch ESG News Feed.")
        # try:
        #     fetch_esg_today_episodes()
        #     logger.info("Ran job: fetch esg today Feed.")
        # except:
        #     logger.info("job FAILED: fetch esg today Feed.")
        # # -------------
        # fetch_scaledagilefrmework_news_items()
        # logger.info("Ran job: fetch scaledagilefrmework Feed.")
        # fetch_agile_alliance_news_items()
        # logger.info("Ran job: fetch agile_alliance Feed.")
        # fetch_101ways_news_items()
        # logger.info("Ran job: fetch 101ways Feed.")
        # fetch_leadinagile_news_items()
        # logger.info("Ran job: fetch leadinagile Feed.")
        body_text = collect_live_rss_feeds()
        body_text = body_text + "\nRan job: Collect RSS Feeds.\n"
        logger.info("Ran job: Collect RSS Feeds.")


        # Send email notification that job has completed
        try:
            send_email(body_text)
            logger.info("Ran job: email notification")
        except:
            logger.info("FAILED job: email notification")



