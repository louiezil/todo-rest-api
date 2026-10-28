from flask import Flask
from config import Config
from database import conn_cursor, create_tables
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.tasks_routes import task_bp
# create app
app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
# load config

app.config.from_object(Config)

# attaCH JWT TO APP

jwt = JWTManager(app)


# load connection and create tables

conn, cursor = conn_cursor()
create_tables(conn, cursor)


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
    
