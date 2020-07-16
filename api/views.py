# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from data.connection import db_connection
from sqlite3 import Error

api = Blueprint('api', __name__)


@api.route("/books", methods=["GET", "POST"])
def books():
    conn = db_connection()
    cur = conn.cursor()
    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM book")
        result = [
            dict(id=row[0], author=row[1], title=row[2],
            shortDescription=row[3], thumbnailUrl=row[4], status=row[5],
            pageCount=row[6])
            for row in cursor.fetchall()
        ]
        if result is not None:
            return jsonify(result)

    if request.method == "POST":
        new_author = request.form["author"]
        new_title = request.form["title"]
        new_sDescription = request.form["shortDescription"]
        new_Url = request.form["thumbnailUrl"]
        new_status = request.form["status"]
        new_pageCount = request.form["pageCount"]

        sql = """INSERT INTO book (author, title, shortDescription, thumbnailUrl,
        status, pageCount)
                 VALUES (?, ?, ?, ?, ?, ?)"""
        cursor = cur.execute(sql, (new_author, new_title, new_sDescription,
        new_Url, new_status, new_pageCount))
        conn.commit()
        conn.close()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201


@api.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = {}
    if request.method == "GET":
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        book = {
            "id": book[0],
            "author": book[1],
            "title": book[2],
            "shortDescription": book[3],
            "thumbnailUrl": book[4],
            "status": book[5],
            "pageCount": book[6],
            
        }
        conn.close()
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404
    if request.method == "PUT":
        sql = """UPDATE book
                SET author=?,
                    pageCount=?,
                    shortDescription=?,
                    status=?,
                    thumbnailUrl=?,
                    title=?
                WHERE id=? """
        author = request.form["author"]
        pageCount = request.form["pageCount"]
        shortDescription = request.form["shortDescription"]
        status = request.form["status"]
        thumbnailUrl = request.form["thumbnailUrl"]
        title = request.form["title"]
        updated_book = {
            "id": id,
            "author": author,
            "pageCount": pageCount,
            "shortDescription": shortDescription,
            "status": status,
            "thumbnailUrl": thumbnailUrl,
            "title": title,
        }
        conn.execute(sql, (author, pageCount, shortDescription,
        status, thumbnailUrl, title, id))
        conn.commit()
        conn.close()
        return jsonify(updated_book)

    if request.method == "DELETE":
        sql_query = "DELETE FROM book WHERE id=?"
        try:
            conn.execute(sql_query, (id,))
            conn.commit()
            conn.close()
            return 'Done with delete'
        except Error:
            print(Error.__name__)
            raise Error
