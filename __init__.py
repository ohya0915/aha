from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_restful_swagger_2 import Api
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from config import Config, config
import os


instance_config = os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance/config.py")
app = Flask(__name__,  static_folder='static', instance_path=instance_config)
app.config.from_object(config['default'])
app.config.from_pyfile('config.py', silent=True)


db = SQLAlchemy(app)
api = Api(app, api_version='0.0', api_spec_url='/api/swagger')
CORS(app, supports_credentials=True)
oauth = OAuth(app)

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


@app.route('/restful_swagger')
def show_swagger():
    return """
    <head>
    <meta http-equiv="refresh" content="0; url=http://petstore.swagger.io/?url=http://127.0.0.1:8000/api/swagger.json" />
    </head>
    """

def create_app():
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from main.routes import main
    app.register_blueprint(main)

    from async_works import send_welcome_mail

    return app