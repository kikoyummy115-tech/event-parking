from flask import Flask
from extension import db, migrate, login_manager
from config import Config
import cloudinary

login_manager.login_view = 'auth.login'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


    # Initialize Cloudinary using app config
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
        secure=True
    )
    
    from app.models.event import Event, Zone, Book
    from app.models.user import User
    from app.models.rag_model import Conversation, Message, Document, DocumentChunk

    with app.app_context():
        db.create_all()

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.chatbot import main

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(main, url_prefix="/")
    

    return app