from flask import Flask
from flask_migrate import Migrate
from models import db, bcrypt

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tuinue_wasichana.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'super-secret-key'  # Update with secure key in production

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")
