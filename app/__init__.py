from flask_login import LoginManager
from flask import Flask
import os



# mongo = PyMongo(app)
# mongo_db = MongoEngine(app)

def create_app(**kwargs):
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="lighter",
        DATABASE="mongodb://127.0.0.1:27017/peddlerdb"),
#     app.config['MONGODB_SETTINGS'] = {
#     'db': 'peddlerdb',
#     'host': 'mongodb://127.0.0.1:27017/peddlerdb'

# }

    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # from . import db
    # from . import auth_routes
    # from . import routes
    # app.register_blueprint(routes.main_bp)
    # app.register_blueprint(auth_routes.bp)
    
    @app.route('/hello')
    def hello():
        return "Hello, world!"
    
    
    
    return app



    


