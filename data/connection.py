import sqlite3


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("/Users/abdul/PycharmProjects/BookLi/books.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn
