import pymysql as pymysql


class Database:
    # Class variables
    cnxn = ""
    cursor = ""

    # Connect to the database on Initialization after assigning the class variables
    def __init__(self, host, user, password, database):
        self.cnxn = pymysql.connect(host, user, password, database)
        self.cursor = self.cnxn.cursor()

    # Create all the necessary tables
    def create_tables(self):
        item_table_sql = "CREATE TABLE IF NOT EXISTS item(" \
                         "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT," \
                         "ebay_id VARCHAR(50)," \
                         "title VARCHAR(255)," \
                         "price DECIMAL(10,2)," \
                         "date DATETIME)"
        sync_table_sql = "CREATE TABLE IF NOT EXISTS sync(" \
                         "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT," \
                         "date DATETIME," \
                         "item_count INT)"
        self.cursor.execute(item_table_sql)
        self.cursor.execute(sync_table_sql)

    # Insert all the items in the item table
    def insert_items(self, items):
        for item in items:
            sql = 'INSERT INTO item (ebay_id, title, price, date) VALUES (%s, %s, %s, %s)'
            val = (item.ebay_id, item.title, item.price, item.date)
            self.cursor.execute(sql, val)
        self.cnxn.commit()

    # Insert a new row in teh sync table
    def insert_sync(self, date, item_count):
        sql = 'INSERT INTO sync (date, item_count) VALUES (%s, %s)'
        val = (date, item_count)
        self.cursor.execute(sql, val)
        self.cnxn.commit()
