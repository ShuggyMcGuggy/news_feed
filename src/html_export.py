# This module provides the functional to enable the export
# of HTML from Django to static HTML files
import requests
from content_aggregator.settings import BASE_DIR


def export_page( source_page_url, output_file):
    response = requests.get(source_page_url)
    # Check the page is valid: if not then return NOT FOUND
    print(response.status_code)
    print(BASE_DIR)
    print('******')
    print(response.content)
    with open(output_file, 'w') as static_file:
        static_file.write(response.text)