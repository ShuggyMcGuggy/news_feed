# Invetigate using requests
"""This file will be used to check requests and the reposnses and
investigate why the rel pth"""

import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from dateutil import parser

import feedparser
#from podcasts.models import NewsItem





url_git = 'https://api.github.com'
url_pods = "https://realpython.com/podcasts/rpp/feed"
url_india = "https://feeds.bcast.fm/the-tastes-of-india"
url_4 ='http://www.reddit.com/r/python/.rss'
url_agile = 'http://www.scaledagileframework.com/feed/'

l_urls_rss_feeds =['https://www.agilealliance.org/feed',
    'https://blog.gitscrum.com/feed/',
    'https://www.agil8.com/feed/',
    'https://www.scrumexpert.com/feed/',
    'https://www.101ways.com/feed/'
    ]

def read_podcasts(url_link):
    feed = feedparser.parse(requests.get(url_link, headers={'User-Agent': 'Mozilla/5.0'}).content)
    print('URL Link: ' + url_link)
    podcast_title = feed.channel.title
    #podcast_image = feed.channel.image["href"]

    for item in feed.entries[:1]:
        print(item.keys())
        print("Title : " + item.title)
        print("GUID: " + item.guid)
        print('Pub Date: ' + item.published)
        print('Parsed Pub Date: ' + str(item.published_parsed))

def explore_feed(url_link):
    feed = feedparser.parse(requests.get(url_link, headers={'User-Agent': 'Mozilla/5.0'}).content)
    if feed:
        for item in feed.entries[:1]:
            print(item.keys())
            print('Title: ' + item.title)
            print('Link: ' + item.link)
            print('Comments: ' + item.comments)
            pub_date = parser.parse(item.published)
            print('Pub Date: ' + item.published)
            print('Parsed Pub Date: ' + str(pub_date))

    else:
        print("Nothing found in feed", url)





# *******  Main  *****
# read_podcasts(url_pods)

explore_feed(url_agile)
for url_feed in l_urls_rss_feeds:
    read_podcasts(url_feed)


# for item in feed.entries:
#     if not Episode.objects.filter(guid=item.guid).exists():
#         episode = Episode(
#             title=item.title,
#             description=item.description,
#             pub_date=parser.parse(item.published),
#             link=item.link,
#             image=podcast_image,
#             podcast_name=podcast_title,
#             guid=item.guid,
#         )



# feed = feedparser.parse(requests.get(url_pods, headers={'User-Agent': 'Mozilla/5.0'}).content)
#
# # feed = feedparser.parse(requests.get(url_4))
# if feed:
#     for item in feed["items"]:
#         link = item["title"]
#         print(link)
# else:
#     print("Nothing found in feed", url)


# only_tags_with_title = SoupStrainer("title")
#
# response = requests.get(url_pods)
#
# if response:
#     print('Success!')
# else:
#     print('An error has occurred.')
#
# print(response.status_code)
# print("******")
# print(response.text)

# r_dict = response.json()
# type(r_dict)
# for key in r_dict.keys():
#     print(key)

# soup = BeautifulSoup(response.text, 'lxml', parse_only=only_tags_with_title)
# items = soup.find_all('item')
# print(items)

# titles = soup.find_all()
# print(titles)

