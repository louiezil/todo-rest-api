import os


class Config:
    DATABASE = "data.db"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"



    #jwt keys
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 86400