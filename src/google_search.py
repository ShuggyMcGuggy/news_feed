
# imports
from googlesearch import search
import xml.etree.ElementTree as ET
import requests
# ****** Functional Definitions ********
def retrieve_links(str_query):
    my_results_list = []
    for i in search(query,        # The query you want to run
                    tld = 'com',  # The top level domain
                    lang = 'en',  # The language
                    num = 10,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 20,  # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                    verify_ssl = False
                   ):
        my_results_list.append(i)
        print(i)
    return my_results_list

# *** Pull an news xml file and parse it ***
def pull_news(url):
    r = requests.Session()


    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Host": "httpbin.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    }
    print(headers)
    r.headers = headers

    try:
        response = r.get(url, headers=headers)
    except:
        response = None
    #response = requests.get("https://httpbin.org/xml")
    print(response.text)

    # soup = bs4.BeautifulSoup(response.text, "html.parser")
    #
    # string_xml = response.content
    # tree = ET.fromstring(string_xml)
    # ET.dump(tree)
    return response


# ***** main code ******

response = pull_news('https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en')
print(response.content)


