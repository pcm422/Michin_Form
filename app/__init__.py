from config import db
from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api

migrate = Migrate()

def create_app():
    application = Flask(__name__)    

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)
    
    api = Api(application)
    
    from app.routes import user_bp, questions_bp, image_bp, choices_bp
    api.register_blueprint(user_bp)
    api.register_blueprint(questions_bp)
    api.register_blueprint(image_bp)
    api.register_blueprint(choices_bp)
    
    return application
