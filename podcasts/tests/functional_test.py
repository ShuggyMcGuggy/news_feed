import unittest
from django.urls import resolve
from django.http import HttpRequest
from selenium import webdriver
from podcasts.views import HomePageView, home

import sys

# adding Folder_2 to the system path
sys.path.insert(0, '/Users/markshury-smith/Development/PyCharmProjects/news_feed')
from podcasts.models import NewsItem


# class NewVisitorTest(unittest.TestCase):
#     '''
#     Confirm the Commentator local server is available.
#     - The Title includes Commentator
#     '''
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def test_can_open_news_list(self):
#         # User opens home page
#         self.browser.get('http://localhost:8000/')
#
#         # The page Title states this is the Commentator Web Site
#         self.assertIn('Commentator', self.browser.title)
#         # self.fail('Finish The Test')

class CommentatorURLTest(unittest.TestCase):
    '''
    Check that key pages for the commentator service are working
    - URLS: Checkl that they resolve
    - Pages: Check the content of the pages is as expected
    '''

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)

        html = response.content.decode('utf8')
        self.assertIn('<title>Commentator</title>',html, "Title is not correct")
        self.assertTrue(html.endswith('</html>'))





if __name__ == '__main__':
    unittest.main()
