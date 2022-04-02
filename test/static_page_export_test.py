import unittest
import requests
from content_aggregator.settings import BASE_DIR


class TestStaticPageSave(unittest.TestCase):
    def test_collect_page(self):
        response = requests.get('https://frozen-brushlands-72168.herokuapp.com/pub_item/2/')
        print(response.status_code)
        print(BASE_DIR)
        print('******')
        print(response.content)
        with open( str(BASE_DIR) + '/static_website/test_file.html', 'w') as static_file:
            static_file.write(response.text)

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()