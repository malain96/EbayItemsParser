class Item:
    # Class variables
    ebay_id = ""
    title = ""
    price = ""
    date = ""

    # Constructor
    def __init__(self, ebay_id, title, price, date):
        self.ebay_id = ebay_id
        self.title = title
        self.price = price
        self.date = date

