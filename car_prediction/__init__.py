
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from car_prediction.config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager






server = Flask(__name__)
server.config.from_object(Config)




login_manager = LoginManager()
login_manager.init_app(server)
db = SQLAlchemy(server)


login_manager = LoginManager()
#login_manager.login_view = 'login'

login_manager.init_app(server)



with server.app_context():
    db.create_all()

from car_prediction import routes 


# application = DispatcherMiddleware(
#     server,
#     {"/app1": app1.server, "/app2": app2.server},
# )

with server.app_context():
    from car_prediction.plotly_dash_apps.routes import dash_blue_print
    server.register_blueprint(dash_blue_print)
    

    from car_prediction.plotly_dash_apps.dashboard2 import create_app_two
    from car_prediction.plotly_dash_apps.dashboard1 import create_app_one

    application = create_app_two(server)
    application = create_app_one(application)

    

