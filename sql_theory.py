import sqlite3
from pprint import pprint

with sqlite3.connect('new_db444.sqlite3') as connection:
    cursor = connection.cursor()

    # query = """
    #     CREATE TABLE IF NOT EXISTS user(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #         name TEXT NOT NULL,
    #         login TEXT NOT NULL CHECK (length(login) > 3) UNIQUE,
    #         password TEXT NOT NULL
    #     )
    # """
    # another_table = """
    # -- CREATE TABLE IF NOT EXISTS category(
    #     --    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #     --    name TEXT NOT NULL
    #     -- );
    #
    # """
    # # cursor.execute(query)
    #
    # query = """
    #     CREATE TABLE IF NOT EXISTS device(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #         title TEXT NOT NULL UNIQUE,
    #         whole_price FLOAT CHECK (whole_price > 0),
    #         price  FLOAT CHECK (price >= whole_price),
    #         category_id INTEGER,
    #         FOREIGN KEY (category_id) REFERENCES category(id)
    #
    #     )
    # """
    # # cursor.execute(query)
    #
    #
    # # CREATE
    # insert_query = """
    #     INSERT INTO category (name)
    #     VALUES (?)
    # """
    # # cursor.execute(insert_query, ['new category'])
    #
    # insert_query_device = """
    #     INSERT INTO device (title, whole_price, price, category_id)
    #     VALUES (?, ?, ?, ?)
    # """
    #
    # # cursor.execute(insert_query_device, ['Samsung A50', 7000, 8000, 1])
    # devices = [
    #     ('Samsung A60', 8000, 8000, 1),
    #     ('Serfing', 3000, 4000, 5),
    # ]
    # # cursor.executemany(insert_query_device, devices)
    #
    #
    # # READ
    # query = """
    #     SELECT title, price
    #     FROM device
    # """
    # query = """
    #     SELECT title, price
    #     FROM device
    #     WHERE price > 5000
    #     LIMIT 2
    #     OFFSET 1
    # """
    # query = """
    #     SELECT title, price
    #     FROM device
    #     WHERE (price > 5000 OR title = 'Serfing') AND (title NOT LIKE '%iPhone%')
    # """
    # result = cursor.execute(query)
    # # pprint(result.fetchall(), indent=4)
    # # pprint(result.fetchall(), indent=4)
    #
    # # pprint(result.fetchmany(size=299), indent=4)
    # pprint(result.fetchone(), indent=4)
    # pprint(result.fetchone(), indent=4)
    # pprint(result.fetchone(), indent=4)






