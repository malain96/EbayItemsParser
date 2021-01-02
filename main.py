import datetime
import os

from classes.database import Database
from classes.soup import Soup
from dotenv import load_dotenv

if __name__ == '__main__':
    # Load .env variables
    load_dotenv()
    # Initialize all variables
    run = True
    current_date = datetime.datetime.now()
    current_page = 1
    items_per_page = 50
    items = []
    total_items = 0
    while run:
        # Get the HTML of the first page of items from ebay
        soup = Soup.get_page_soup(current_page, items_per_page)
        # Get the total amount of items from ebay
        if total_items == 0:
            total_items = int(soup.find('span', class_='rcnt').get_text())
        # Check if there is a next page
        # If it's the case, add 1 to current_page
        if items_per_page * current_page < total_items:
            current_page += 1
        # If it's not, change run to false
        else:
            run = False

        # Get all items from the html
        html_items = soup.find_all(
            'li', id=lambda value: value and value.startswith('item'))
        for i in html_items:
            items.append(Soup.get_item(i, current_date))

    # Create the connection to the DB
    db = Database(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
    # Create the tables if they don't exist
    db.create_tables()
    # Insert all items
    db.insert_items(items)
    # Insert a sync entry
    db.insert_sync(current_date, total_items)
