import sqlite3

conn = sqlite3.connect("/Users/abdul/PycharmProjects/BookLi/books.sqlite")
cursor = conn.cursor()

sql_query = """CREATE TABLE BOOK (
    id integer PRIMARY KEY,
    author text NOT NULL,
    title text NOT NULL,
    shortDescription text NOT NULL,
    thumbnailUrl text NOT NULL,
    statud text NOT NULL,
    pageCount integer NOT NULL
)"""
cursor.execute(sql_query)
