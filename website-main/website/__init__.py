from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
from os import path
from flask_login import LoginManager
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

db = SQLAlchemy()
DATABASE = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    ##create local SQLite database##    
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'

    ##create MySQL database##    
    load_dotenv()
    connection_string = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # Set the app's database connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    # Bind the SQLAlchemy instance to this Flask app
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

        def create_admin():
            admin = User.query.filter_by(first_name='admin').first()
            if not admin:
                # Create the admin user with default values
                first_name='admin'
                email='admin@admin.com'
                password='Black!Hole123'
                new_admin = User(first_name=first_name, email=email, 
                                 password=generate_password_hash(password, method='sha256'), 
                                 status='active', account_type='admin')
                db.session.add(new_admin)
                db.session.commit()

        create_admin()  # Call the function directly

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
