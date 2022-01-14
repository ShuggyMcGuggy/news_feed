import feedparser
# import pprint

from pygooglenews import GoogleNews

# gn = GoogleNews()
# top = gn.top_news(proxies=None, scraping_bee = None)
# for item in top.entries:
#     print(item)

feed = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
# feed = feedparser.parse('https://news.google.com/rss.xml')
numberOfHeadlines = len(feed['entries'])

# print ("Feed title is: " + podcast_title)

for i in range(0,numberOfHeadlines):
    print(feed['entries'][i]['title'])




