# This module pulls the data from the targetted web sites
from gnewsclient import gnewsclient

client = gnewsclient.NewsClient(language='english',
                                location='',
                                topic='agile methodology',
                                max_results=10)

news_list = client.get_news()

for item in news_list:
    print("Title : ", item['title'])
    print("Link : ", item['link'])
    print("")