import os
import re
import requests

from bs4 import BeautifulSoup
from ebayItemsParser.item import Item


class Soup:
    # Get all the info from the HTML and return an item
    @staticmethod
    def get_item(html_item, date):
        title = html_item.find('h3', class_='lvtitle').contents[0].get_text()
        price_string = html_item.find('li', class_='lvprice').get_text().replace(',', '.').strip()
        price = float(re.findall('\\d+\\.\\d+', price_string)[0])
        return Item(html_item.get('id'), title, price, date)

    # Get and return the HTML from the URL
    @staticmethod
    def get_page_soup(page, items_count):
        # Calculate the amount of item to skip (used in the URL)
        skip_count = (page - 1) * items_count
        url = os.getenv("URL").format(page, skip_count)
        req = requests.get(url)
        return BeautifulSoup(req.text, 'html.parser')
