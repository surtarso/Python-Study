from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

#create and initialize database
db = SQLAlchemy()
DB_NAME = 'database.db'

# initialize flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-123j1hj2b4uj1gh23v4ghjv23hm4gv'
    #database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #tells flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  #what user are we looking for
    
    return app

#create the database
def create_database(app):
    #if it doesnt exist already
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('A NEW DATABASE WAS CREATED')
        