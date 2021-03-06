from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import environ
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sup3rn0va01@34.89.36.49:3306/Books'

# app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://' + getenv('MYSQL_USER') + ':' + getenv('MYSQL_PASS') + '@' + getenv('MYSQL_URL') + '/' + getenv('MYSQL_DB'))
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from application import routes
