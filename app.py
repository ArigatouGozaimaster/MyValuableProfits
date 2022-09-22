"""
Importing Libraries
-------------------

Import the necessary libraries for the program to run. A full list of requirements can be found 
under requirements.txt. For more details, consult the attached ReadMe.md
"""

import re
import yfinance as yf
import sqlite3

from pandas_datareader import data
from flask import Flask, render_template, url_for, redirect, request
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

# Prepare SQLAlchemy Database
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
- Get LIVE Exchange Rate Data (data.DataReader)
- Fetch LIVE Stock Price (YFinance)
- Fetching an Exchange Rate from the past 1300 days (LIMIT)
- Clean up User_id to only return integer
"""

# Get LIVE Exchange Rate Data (data.DataReader)
def current_rate():
    AUD = data.DataReader('DEXUSAL', 'fred')

    # Returns latest entry in exchange rate panda dataform
    current_exchange_rate = AUD.DEXUSAL.iat[-1]
    return current_exchange_rate

# Fetch LIVE Stock Price (YFinance)
def price_fetch(stock):
    ticker = yf.Ticker(str(stock).upper())

    # if ticker does not exist:
    if ticker.info['regularMarketPrice'] is None:
        return ValueError

    # if ticker is Australian with .AX
    elif ".AX" in stock:
        return round(ticker.info['regularMarketPrice'], 2)

    # if ticker is NASDAQ, convert to AUD 
    else:
        return round(ticker.info['regularMarketPrice'] / current_rate(), 2)

app.jinja_env.globals.update(price_fetch = price_fetch)

# Fetching an Exchange Rate from the past 1300 days (LIMIT)
def historic_exchange_rate(purchase_date):
    df = data.DataReader('DEXUSAL', 'fred')
    try:
        value = df.loc[purchase_date, 'DEXUSAL']
    except KeyError:
        value = current_rate() 
    return value

# Clean up User_id to only return integer
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
- Search Yahoo Finance (/yahoofinance)
"""


@app.route('/')
def home():
    """ Redirect user to the login page """

    return login()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Show the login page and prompt the user to login """

    form = LoginForm()

    # Username Validation
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # If username exists in the database
        if user:

            # If password is valid
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)

                # Redirect to user dashboard
                return redirect(url_for('dashboard'))

            # If password does not match
            else:
                error_msg = "Invalid password"
                return render_template('login.html', form = form, error_msg = error_msg)

        # If username does not exist in the database
        else:
            error_msg = "Invalid username"
            return render_template('login.html', form = form, error_msg = error_msg)

    # GET Request
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Show the register page and prompt the user to register """

    form = RegisterForm()

    # POST Request
    if request.method == 'POST':

        # Check new user valid and register to database.db 
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
        # If username has already been taken
        else:
            error_msg = "Username is already taken"
            return render_template('register.html', form = form, error_msg = error_msg)

    # GET Request
    if request.method == 'GET':
        return render_template('register.html', form = form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """ Users to logout of their account """

    # Logout the user
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
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
    
    # Fetch current exchange rate price
    exchange_rate = current_rate()

    # Fetch Portfolio Information for current user stored in SQL
    fetch_database = cur.execute("SELECT ticker, name, market, avgprice, quantity, brokerage FROM portfolio WHERE user_id = ?", (user_name,))
    fetch_database = cur.fetchall()

    # Sanity check if there are any holdings (at all)
    if fetch_database:
        get_data = list(fetch_database)


        # Iterating the database for each information field (Debug Test)
        for information in get_data:

            # Iterate for ticker
            ticker = information[0]

            # Iterate for the full stock name
            name = information[1]

            # Iterate for the market it belongs to
            market = information[2]

            # Iterate for the average price the user has paid for the stock
            avgprice = information[3]

            # Iterate for the quantity of holdings
            quantity = information[4]

    return render_template('dashboard.html', user = user_name, exchange_rate = exchange_rate, get_data = get_data)

    

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    
    # Fetch information from form
    if request.method == 'POST':
        formdata = request.form

        # Fetch ticker information and change it to uppercase
        ticker = formdata["ticker"].upper()

        # Fetch user defined purchase price
        price = round(float(formdata["price"]),2)

        # Fetch user defined amount of stocks
        amount = float(formdata["amount"])

        # Fetch user defined purchase date. This will be used to fetch an exchange rate
        date = formdata["date"]

        # Fetch user defined brokerage
        brokerage = round(float(formdata["brokerage"]),2)

        # Check validity of "Ticker"
        if price_fetch(ticker) is ValueError:
            return render_template("error.html")

        # Check validity of "Price"
        if isinstance(price, float) is False:
            return render_template("error.html")
        
        # Check validity of "Amount"
        if isinstance(amount, float) is False:
            return render_template("error.html")

        # Check validity of "Brokerage"
        if isinstance(brokerage, float) is False:
            return render_template("error.html")
        
        # Get full name of stock
        symbol = yf.Ticker(ticker)
        company_name = symbol.info['longName']
        print(company_name)

        # Put Market Locale (Only supports AX and NYSE)
        if ".AX" in ticker:
            marketindex = "ASX"
        
        # Assumes user understands only ASX and NYSE are allowed
        else:
            marketindex = "NYSE"
        
        # Adjust for exchange rate
        if not ".AX" in ticker:
            exchange_rate = historic_exchange_rate(str(date))
            price = price / exchange_rate

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
            new_avg = round((existing_value + new_value)/(new_quantity),2)

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

    return dashboard()

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():

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
            return render_template("error.html")

        # Check validity of "Price"
        if isinstance(price, float) is False:
            return render_template("error.html")
        
        # Check validity of "Amount"
        if isinstance(amount, float) is False:
            return render_template("error.html")

        # Check validity of "Brokerage"
        if isinstance(brokerage, float) is False:
            return render_template("error.html")
        
        # Get full name of stock
        symbol = yf.Ticker(ticker)
        company_name = symbol.info['longName']
        print(company_name)

        # Adjust for exchange rate
        if not ".AX" in ticker:
            exchange_rate = historic_exchange_rate(str(date))
            price = price / exchange_rate
        
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
        
        # Validity check for stock existing in portfolio
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
            
            # Validity check that owned stocks >= sold stocks
            if update_quant >= amount:

                # Calculate new values for SQL database
                new_quantity = update_quant - amount
                new_brokerage = update_brokerage + brokerage
                existing_value = update_quant * update_avg
                new_value = amount * price

                # Calculates new quantity and avoids zero division error
                if new_quantity == 0:
                    new_avg = 0
                else:
                    new_avg = round((existing_value - new_value)/(new_quantity),2)

                # Update SQL database
                cur.execute("UPDATE portfolio SET quantity = ?, brokerage = ?, avgprice = ? WHERE ticker = ? AND user_id = ?", 
                       (new_quantity, new_brokerage, new_avg, ticker, user_name))
                con.commit()
        
    return dashboard()

@app.route('/yahoofinance', methods=['GET', 'POST'])
@login_required
def yahoofinance():
    if request.method == 'POST':

        # Retrieve the information that the user inputted on the searchbar
        formdata = request.form
        ticker = str(formdata["yahoo_check"])

        # Query Yahoo Finance directly for the string that the user inputted
        ticker = "https://finance.yahoo.com/lookup?s="+ticker

        return redirect(ticker)
        

if __name__ == '__main__':
    app.run(debug=True)
