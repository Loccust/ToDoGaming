from flask import Flask, redirect
from flask_jwt_extended import JWTManager
from flask_restful import Api

from src.auth.routes import auth_bp
from src.config import Config
from src.models import db
from src.resources.task_resource import TaskListResource, TaskResource
from src.resources.user_resource import ProfileResource
from src.config.swagger_config import swagger_config, swagger_template

from flasgger import Swagger


def init_app():
    app: Flask = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    JWTManager(app)
    api = Api(app)
    Swagger(app, config=swagger_config, template=swagger_template)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)

    api.add_resource(TaskListResource, '/tasks')
    api.add_resource(TaskResource, '/tasks/<int:task_id>')
    api.add_resource(ProfileResource, '/profile')

    @app.route('/')
    def redirect_to_docs():
        return redirect('/apidocs')

    return app