from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:oz-password@127.0.0.1/mini_michin_form"    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_ECHO = False
    
    # Swagger 설정
    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    reload = True  