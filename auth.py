import re

from flask import Blueprint, render_template, request, session, message_flashed, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from data.connection import db_connection


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    conn = db_connection()
    cur = conn.cursor()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        print('login req get')
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE email=? and password=?"
        cur.execute(sql, (email, password))
        account = cur.fetchone()
        print(account)
        if account:
            session['logged_in'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            session['name'] = account[3]
            # flash('LoggedIn successfully!')
            return redirect(url_for('website.home'))
    if request.method == 'GET':
        return render_template('login.html')


@auth.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('website.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = db_connection()
    cur = conn.cursor()
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        password = generate_password_hash(password)
        email = request.form['email']
        sql = "SELECT * FROM user WHERE email=? and password=?"
        cur.execute(sql, (email, password))
        account = cur.fetchone()
        if account:
            msg = 'You already have an account, login please!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            sql = "INSERT INTO user VALUES (NULL, ?, ?, ?)"
            cur.execute(sql, (email, password, name))
            conn.commit()
            conn.close()
            flash('You have successfully registered!')
            return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('signup.html', msg=msg)
