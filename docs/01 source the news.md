# Ideninty sources: pull data

## Admin Accoutn
markshury-smith
Sack((345Boot))
Sack((345Boot))

## What is news aggregator ?
A news aggregator is a system that takes news from several resources and puts them all together. A good example of news aggregator are JioNews and Google News.
## Why build a news aggregator ?
There are hundreds of news websites, they do cover news on serveral broad topics, out of which only a few of them are of our interest. A news aggregator can be a tool to save a lot of time and with some modifications and filteration we can fine tune it to show only news of our interest.

A news aggregator can be an useful tool to get information within short time.
## Plan
We'll build our news aggeragator in 3 parts. These are following:

We'll research on html source code of news sites and build a website scrapper for each
Then, We'll setup our django server
Finally, we'll integrate everything altogether
So, let's start with first step.

## Resources
- [link to news aggregator project](https://www.hackersfriend.com/articles/building-news-aggregator-web-app-with-django-using-python-web-scraping)
- [link to Django news aggregator project](https://realpython.com/build-a-content-aggregator-python/)
- [How to write google searches in python](https://towardsdatascience.com/current-google-search-packages-using-python-3-7-a-simple-tutorial-3606e459e0d4)
- [Django getting started](https://realpython.com/get-started-with-django-1/)
- [Beautiful Soup web scraper](https://realpython.com/beautiful-soup-web-scraper-python/)
- [Markdown code syntax](https://daringfireball.net/projects/markdown/syntax#precode)
- [Details for the google news API](https://newscatcherapi.com/blog/google-news-rss-search-parameters-the-missing-documentaiton)
- [Tutorial site W3 Schools](https://www.w3schools.com/python/python_try_except.asp)
- [Scraping news from google news](https://medium.com/analytics-vidhya/google-scraping-using-beautifulsoup-d53746ef5a32)


#Building the website scrapper
Before we start building scrapper, let's get the required packages first. You can install them from command prompt by these commads.

<code>pip install bs4</code><br>
<code>pip install requests </code><br>
<code>pip install google</code>

This will install the required packages.

GUI front end
https://towardsdatascience.com/top-10-python-gui-frameworks-for-developers-adca32fbe6fc
https://www.geeksforgeeks.org/build-an-application-to-extract-news-from-google-news-feed-using-python/