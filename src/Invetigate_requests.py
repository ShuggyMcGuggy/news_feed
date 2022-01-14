# Invetigate using requests
"""This file will be used to check requests and the reposnses and
investigate why the rel pth"""

import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import feedparser
# from podcasts.models import Episode




url_git = 'https://api.github.com'
url_pods = "https://realpython.com/podcasts/rpp/feed"
url_india = "https://feeds.bcast.fm/the-tastes-of-india"
url_4 ='http://www.reddit.com/r/python/.rss'
url_agile = 'http://www.scaledagileframework.com/feed/'

feed = feedparser.parse(requests.get(url_pods, headers={'User-Agent': 'Mozilla/5.0'}).content)
podcast_title = feed.channel.title
podcast_image = feed.channel.image["href"]

for item in feed.entries:
    print("Title : " + item.title)
    print("GUID: " + item.guid)

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

# feed = feedparser.parse(requests.get(url_4))
# if feed:
#     for item in feed["items"]:
#         link = item["link"]
#         print(link)
# else:
#     print("Nothing found in feed", url)

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

