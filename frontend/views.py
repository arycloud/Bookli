# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, redirect, url_for
from data.connection import db_connection
from functools import wraps
from flask import session, flash

website = Blueprint('website', __name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            # flash("You need to login first")
            return redirect(url_for('auth.login'))

    return wrap


@website.route("/")
def home():
    conn = db_connection()
    cur = conn.cursor()
    cursor = conn.execute("SELECT * FROM book")
    result = [
        dict(id=row[0], author=row[1], title=row[2],
             shortDescription=row[3], thumbnailUrl=row[4], status=row[5],
             pageCount=row[6])
        for row in cursor.fetchall()
    ]
    if result is not None:
        return render_template('home.html', books=result)


@website.route("/books", methods=["GET", "POST"])
@login_required
def books():
    conn = db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        new_author = request.form["author"]
        new_title = request.form["title"]
        new_sDescription = request.form["shortDescription"]
        new_tUrl = request.form["thumbnailUrl"]
        new_status = request.form["status"]
        new_pageCount = request.form["pageCount"]

        sql = """INSERT INTO book (author, title, shortDescription, thumbnailUrl,
        status, pageCount)
                         VALUES (?, ?, ?, ?, ?, ?)"""
        cursor = cur.execute(sql, (new_author, new_title, new_sDescription,
                                   new_tUrl, new_status, new_pageCount))
        conn.commit()
        conn.close()
        return redirect(url_for('website.home'), code=302)


@website.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
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
        if book is not None:
            return render_template('book_detail.html', book=book)
        else:
            return "Something wrong", 404


@website.route("/book/<int:book_id>/edit", methods=["GET", "POST", "UPDATE"])
@login_required
def edit_book(book_id):
    conn = db_connection()
    cursor = conn.cursor()
    book = {}
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
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
        return render_template('book_edit.html', book=book)

    if request.method == 'POST':
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
            "id": book_id,
            "author": author,
            "pageCount": pageCount,
            "shortDescription": shortDescription,
            "status": status,
            "thumbnailUrl": thumbnailUrl,
            "title": title,
        }
        conn.execute(sql, (author, pageCount, shortDescription,
                           status, thumbnailUrl, title, book_id))
        conn.commit()
        return redirect(url_for('website.single_book', id=book_id))


@website.route("/book/create")
@login_required
def create_book():
    return render_template('book_create.html')
