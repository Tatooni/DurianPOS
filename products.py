import sqlite3


def connect():
    return sqlite3.connect("durian_pos.db")


# CREATE PRODUCT TABLE
def create_product_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)

    conn.commit()
    conn.close()


# ADD PRODUCT
def add_product(name, price):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (name, price)
    )

    conn.commit()
    conn.close()


# GET PRODUCTS
def get_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return products


# CREATE SALES TABLE
def create_sales_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        total REAL
    )
    """)

    conn.commit()
    conn.close()


# SAVE SALE
def save_sale(date, total):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sales (date, total) VALUES (?, ?)",
        (date, total)
    )

    conn.commit()
    conn.close()

import sqlite3


def connect():
    return sqlite3.connect("durian_pos.db")


# CREATE PRODUCT TABLE
def create_product_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)

    conn.commit()
    conn.close()


# ADD PRODUCT
def add_product(name, price):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (name, price)
    )

    conn.commit()
    conn.close()


# GET PRODUCTS
def get_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return products


# CREATE SALES TABLE
def create_sales_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        total REAL
    )
    """)

    conn.commit()
    conn.close()

# SAVE SALE
def save_sale(date, total):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sales (date, total) VALUES (?, ?)",
        (date, total)
    )

    conn.commit()
    conn.close()

def get_sales():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales")

    sales = cursor.fetchall()

    conn.close()

    return sales

def delete_product(name):

    import sqlite3

    conn = sqlite3.connect("durian_pos.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE name=?", (name,))

    conn.commit()
    conn.close()