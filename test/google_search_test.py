import unittest
import src.google_search as g_s


class Test_Parsing_XML_news(unittest.TestCase):
    def setUp(self) -> None:
        #self.url_google_news = 'https://news.google.com/rss.xml'
        self.url_google_news = 'https://news.google.com/rss.xml'
    def test_xml_data_pull(self):
        response = g_s.pull_news(self.url_google_news)
        self.assertNotEqual(None, response)

class Test_Google_Search_Data_Pull(unittest.TestCase):
    def setUp(self) -> None:
        self.query = "agile risk management 2021"
    def test_google_search(self):
        items = g_s.retrieve_links(self.query)
        self.assertNotEqual([], items)



if __name__ == '__main__':
    unittest.main()
