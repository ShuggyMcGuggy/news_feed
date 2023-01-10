import unittest
from selenium import webdriver

import sys

# adding Folder_2 to the system path
sys.path.insert(0, '/Users/markshury-smith/Development/PyCharmProjects/news_feed')
from podcasts.models import NewsItem

class RCC_websiteTest(unittest.TestCase):
    '''
    Set of test to provide a daily check that the RCC site is up and running
    - Can the home page be accessed?
    '''

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_news_list(self):
        # User opens home page
        self.browser.get('https://www.royalcanoeclub.com//')

        # The page Title states this is the Commentator Web Site
        self.assertIn('Royal Canoe Club – The original canoe club', self.browser.title)
        # self.fail('Finish The Test')


if __name__ == '__main__':
    unittest.main()
