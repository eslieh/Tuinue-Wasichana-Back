from flask import Flask
from flask_migrate import Migrate
from models import db, bcrypt
from dotenv import load_dotenv
from utils import redis_client  
from routes.authentication import auth_bp 
from routes.charity import charity_bp 
from routes.admin import admin_bp
from routes.stories import story_bp
from routes.Donations import donation_bp
from routes.inventory import inventory_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # App configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tuinue_wasichana.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'super-secret-key'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(charity_bp, url_prefix='/charities')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(story_bp, url_prefix='/stories')
    app.register_blueprint(donation_bp, url_prefix='/donations')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)