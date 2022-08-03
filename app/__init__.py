from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

# inits for database management
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# login!
login = LoginManager(app)

# Configure settings
# COME BACK NEED TO CREATRE LOGIN FUNCTION
login.login_view = 'login'
login.login_message = 'Please enter your email and password below'
login.login_message_category = 'warning'

from app import routes, models, forms