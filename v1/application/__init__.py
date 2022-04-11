from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
    
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.app_context():
        from .link import link
        app.register_blueprint(link)
        
        return app