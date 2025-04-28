from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, bcrypt
from dotenv import load_dotenv
from utils import redis_client  
from routes.authentication import auth_bp  

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # allow only your Vite dev server on port 5173
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

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

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)
