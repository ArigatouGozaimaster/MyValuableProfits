### Importing libraries required ###



import os
import datetime
import yfinance as yf

from flask import Flask, flash, render_template, url_for, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



### Configure applications ###



# Initialise
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Prepare Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '$a1teDP@$$w0rd15Very1MP0Rtant'

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Reload the user's object from the user's session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure database.db
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

    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")



### App.Route ###

U = None

@app.route('/')
def home():
    """ Show the default homepage of unregistered user """

    # TODO: Homepage?
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Show the login page and prompt the user to login """

    form = LoginForm()
    global U
    # Login Validation via POST request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        U = form.username.data
        if user:
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


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """ Stock Portfolio Dashboard - Implement Majority of code HERE"""

    # TODO:
    return render_template('dashboard.html', user=U)


if __name__ == '__main__':
    app.run(debug=True)

