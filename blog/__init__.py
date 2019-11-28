from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "find yours"
app.config["SQLALCHEMY_DATABASE_URI"] ='postgresql://postgres:getyours@localhost:5432/flaskblog'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ivobcglifeojjk:8b0c7a01944e476def22801f12bda8d32f4274296dcb77b369c0b35dce245f1b@ec2-107-22-253-158.compute-1.amazonaws.com:5432/d3n1kvvfoj00o6"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from blog import routes