"""
Importing Libraries
-------------------

Import the necessary libraries for the program to run. A full list of requirements can be found 
under requirements.txt. For more details, consult the attached ReadMe.md
"""

import os
import re
import datetime
import yfinance as yf
import sqlite3

from pandas_datareader import data
from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

"""
Configure Applications
----------------------

A list of pre-requisites for functionality
- Initialisation of Flask constructor module, SQLAlchemy, and Bcrypt
- Ensure templates are auto-reloaded
- Configure session to use filesystem (instead of signed cookies)
- Prepare Database
- Link Database to SQLite3
- Login Manager
- Reload the user's object from the user's session
- Configure database.db
- Register for an account
- Register for an account
"""

# Initialisation of Flask constructor module and Bcrypt
app = Flask(__name__, static_url_path='/static')
bcrypt = Bcrypt(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Prepare Database
app.config['SECRET_KEY'] = '$a1teDP@$$w0rd15Very1MP0Rtant'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Link Database to SQLite3
con = sqlite3.connect('database.db', check_same_thread=False, isolation_level=None)
cur = con.cursor()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Reload the user's object from the user's session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure "user" table in database.db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)

# Register for an account
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        if existing_user_username:
            raise ValidationError("This username is already taken. Please choose a different one")

# Login for an account
class LoginForm(FlaskForm):

    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "e.g. admin"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "e.g. admin"})
    
    submit = SubmitField("Login")


"""
Helper Functions
----------------

A list of helper functions for the functionality of the website
- Get LIVE Exchange Rate Data 
- Fetch LIVE Stock Price (YFinance)
- Clean up User_id
"""

# Get LIVE Exchange Rate Data
def current_rate():
    AUD = data.DataReader('DEXUSAL', 'fred')
    current_exchange_rate = AUD.DEXUSAL.iat[-1]
    return current_exchange_rate

# Fetch LIVE Stock Price (YFinance)
def price_fetch(stock):
    ticker = yf.Ticker(str(stock).upper())

    # if ticker does not exist:
    if ticker.info['regularMarketPrice'] is None:
        return ValueError

    # if ticker is Australian
    elif ".ax" in stock:
        return round(ticker.info['regularMarketPrice'], 2)

    # if ticker is NASDAQ, convert to AUD
    else:
        return round(ticker.info['regularMarketPrice'] / current_rate(), 2)

# Clean up User_id
def user_id(input):
    id = re.findall("\d+", input)
    var = ''
    for element in id:
        var += str(element)
    user = int(var)
    return user


"""
App.Route
---------
The backend of all url routing including:
- Landing Page (/)
- Login (/login)
- Register (/register)
- Logout (/logout)
- Dashboard (/dashboard)
- Buy (/buy)
"""


@app.route('/')
def home():
    """ Show the default homepage of unregistered user """

    # TODO: Homepage?
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Show the login page and prompt the user to login """

    form = LoginForm()

    # Username Validation
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:

            # Password Validation
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)

                return redirect(url_for('dashboard'))

    # GET Request
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Show the register page and prompt the user to register """

    form = RegisterForm()

    # Register new user to database.db via POST request
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    # GET Request
    return render_template('register.html', form = form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """ Users to logout of their account """

    # Logout the user
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """ Stock Portfolio Dashboard """

    # Fetch user's id
    current_user_number = str(current_user)

    # Change user's id into a number for reference in SQL database
    user_number = int(user_id(current_user_number))

    # Fetch username from user's id
    user_name = cur.execute("SELECT username FROM user WHERE id = ?", (user_number,))
    user_name = cur.fetchone()

    # Query loop to return only one element
    for name in user_name:
        user_name = name
    return render_template('dashboard.html', user = user_name)

    

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    
    # Fetch information from form
    if request.method == 'POST':
        formdata = request.form
        ticker = formdata["ticker"].upper()
        price = round(float(formdata["price"]),2)
        amount = float(formdata["amount"])
        date = formdata["date"]
        brokerage = round(float(formdata["brokerage"]),2)

        # Check validity of "Ticker"
        if price_fetch(ticker) is ValueError:
            print("ERR1")
            return render_template("error.html")

        # Check validity of "Price"
        if isinstance(price, float) is False:
            print("ERR2")
            return render_template("error.html")
        
        # Check validity of "Amount"
        if isinstance(amount, float) is False:
            print("ERR3")
            return render_template("error.html")

        # Check validity of "Brokerage"
        if isinstance(brokerage, float) is False:
            print("ERR4")
            return render_template("error.html")
        
        # Get full name of stock
        symbol = yf.Ticker(ticker)
        company_name = symbol.info['longName']
        print(company_name)

        # Put Market Locale
        if ".ax" in ticker:
            marketindex = "ASX"
        else:
            marketindex = "NYSE"
        
        # Fetch user's id
        current_user_number = str(current_user)

        # Change user's id into a number for reference in SQL database
        user_number = int(user_id(current_user_number))

        # Fetch username from user's id
        user_name = cur.execute("SELECT username FROM user WHERE id = ?", (user_number,))
        user_name = cur.fetchone()

        # Query loop to return only one element
        for name in user_name:
            user_name = name
        
        # Check for existing stocks of the same category
        existing_stock = cur.execute("SELECT ticker FROM portfolio WHERE ticker = ? AND user_id = ?", (ticker, user_name))
        existing_stock = cur.fetchall()

        # Update an existing entry for the stock
        if existing_stock:

            # Fetch current existing portfolio details [avgprice]
            update_avg = cur.execute("SELECT avgprice FROM portfolio WHERE ticker = ? AND user_id = ?", (ticker, user_name))
            update_avg = cur.fetchone()
            for number in update_avg:
                update_avg = number

            # Fetch current existing portfolio details [quantity]
            update_quant = cur.execute("SELECT quantity FROM portfolio WHERE ticker = ? AND user_id = ?", (ticker, user_name))
            update_quant = cur.fetchone()
            for number in update_quant:
                update_quant = number

            # Fetch current existing portfolio details [brokerage]
            update_brokerage = cur.execute("SELECT brokerage FROM portfolio WHERE ticker = ? AND user_id = ?", (ticker, user_name))
            update_brokerage = cur.fetchone()
            for number in update_brokerage:
                update_brokerage = number

            # Calculate new values for SQL database
            new_quantity = update_quant + amount
            new_brokerage = update_brokerage + brokerage
            existing_value = update_quant * update_avg
            new_value = amount * price
            new_avg = (existing_value + new_value)/(new_quantity)
            print(new_quantity, new_brokerage, new_avg)

            # Sanity Check
            if cur.execute("SELECT * FROM portfolio WHERE ticker = ? AND user_id = ?", (ticker, user_name)):
                print('FOUND')
            else:
                print('NOT FOUND')

            # Update SQL database
            cur.execute("UPDATE portfolio SET quantity = ?, brokerage = ?, avgprice = ? WHERE ticker = ? AND user_id = ?", 
                       (new_quantity, new_brokerage, new_avg, ticker, user_name))
            con.commit()

        # Create brand new entry for stock
        if not existing_stock:

            # Execute SQL insertion
            cur.execute("INSERT INTO portfolio (user_id, ticker, name, market, avgprice, quantity, brokerage, buysell) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_name, ticker, company_name, marketindex, price, amount, brokerage, 'buy'))
            con.commit()

    return render_template('dashboard.html', user = user_name)

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)

