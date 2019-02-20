from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #db obj repr database 
migrate = Migrate(app, db) #repr migration engine
login = LoginManager(app)
login.login_view ='login'
bootstrap = Bootstrap(app)

from App import routes, models
