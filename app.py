from flask import Flask
from config import Config
from database import conn_cursor, create_tables
from flask_jwt_extended import JWTManager
from routes.routes import auth_bp

# create app
app = Flask(__name__)
app.register_blueprint(auth_bp)
# load config

app.config.from_object(Config)

# attaCH JWT TO APP

jwt = JWTManager(app)


# load connection and create tables

conn, cursor = conn_cursor()
create_tables(conn, cursor)


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
    
