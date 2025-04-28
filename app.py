import collections
import collections.abc
collections.Mapping = collections.abc.Mapping


import jwt.algorithms
jwt.algorithms.requires_cryptography = []

import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from models import db, bcrypt
from utils import redis_client
from routes.authentication import auth_bp
from routes.charity import charity_bp

# Load .env variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # App configurations
    # allow only your Vite dev server on port 5173
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tuinue_wasichana.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['SECRET_KEY'])

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(charity_bp, url_prefix='/charities')
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)
