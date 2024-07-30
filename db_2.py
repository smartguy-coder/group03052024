import sqlite3
from pprint import pprint

with sqlite3.connect("new_db2.sqlite3") as connection:
    # cursor = connection.cursor()

    # another_table = """
    #     CREATE TABLE IF NOT EXISTS category(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #         name TEXT NOT NULL
    #     );
    #
    # """
    # cursor.execute(another_table)
    # query = """
    #     CREATE TABLE IF NOT EXISTS products(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #         title TEXT NOT NULL UNIQUE,
    #         whole_price FLOAT CHECK (whole_price > 0),
    #         price  FLOAT CHECK (price >= whole_price),
    #         category_id INTEGER,
    #         FOREIGN KEY (category_id) REFERENCES category(id)
    #     )
    # """
    # cursor.execute(query)

    # CREATE
    # insert_query = """
    #     INSERT INTO category (name)
    #     VALUES (?)
    # """
    # cursor.execute(insert_query, ['new category'])
    #
    # insert_query_device = """
    #     INSERT INTO products (title, whole_price, price, category_id)
    #     VALUES (?, ?, ?, ?)
    # """
    #
    # cursor.execute(insert_query_device, ['Samsung A50', 7000, 8000, 1])
    #
    # devices = [
    #     ('Samsung A60', 8000, 8000, 1),
    #     ('Serfing', 3000, 4000, 5),
    # ]
    # cursor.executemany(insert_query_device, devices)

    # READ
    # query = """
    #     SELECT title, price
    #     FROM products
    # """
    # query2 = """
    #     SELECT title, price
    #     FROM products
    #     WHERE price > 5000
    #     LIMIT 2
    #     OFFSET 2
    # """
    # query3 = """
    #     SELECT title, price
    #     FROM products
    #     WHERE (price > 1000 OR title = 'Serfing') AND (title NOT  LIKE '%5%')
    # """
    # result: list[tuple] = cursor.execute(query3).fetchall()
    # pprint(result, indent=4)

    # UPDATE
    # query1 = """
    #     UPDATE products
    #     SET
    #        category_id = 2
    #     WHERE
    #         price > 5000
    # """
    # query2 = """
    #     UPDATE products
    #     SET
    #        title = UPPER(title),
    #        price = price * 1.2
    #     WHERE
    #         title  LIKE '%5%'
    # """
    # cursor.execute(query2)

    # DELETE
    # query = """
    #     DELETE FROM products
    #     WHERE
    #         title  LIKE '%HHHG%'
    # """
    # cursor.execute(query)

    # DUMP CREATE
    # with open('dump.sql', 'w') as dump:
    #     for sql in connection.iterdump():
    #         dump.write(sql)
    pass


# READ DUMP
with sqlite3.connect("new_db3.sqlite3") as connection2:
    cursor2 = connection2.cursor()
    # with open('dump.sql', 'r') as dump:
    #     sql = dump.read()
    #     cursor2.executescript(sql)

    # RENAME TABLE
    # query = """
    #     ALTER TABLE caregories
    #     RENAME TO categories
    # """
    # cursor2.execute(query)

    # RENAME COLUMN
    # query = """
    #     ALTER TABLE categories
    #     RENAME COLUMN name TO category_name
    # """
    # cursor2.execute(query)

    # ADD COLUMN
    # query = """
    #     ALTER TABLE categories
    #     ADD COLUMN is_premium BOOLEAN DEFAULT FALSE
    # """
    # cursor2.execute(query)

    query = """
        SELECT products.title, products.price * 1.2, categories.category_name
        FROM products        
        LEFT JOIN categories
        ON products.category_id = categories.id
        -- WHERE categories.id = 2
    """
    result = cursor2.execute(query).fetchall()
    pprint(result)
