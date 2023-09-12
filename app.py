import flask
from flask_restful import Api
from resource.user import Users, User
from resource.organisation import Org, Orgs
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from model import db 

# Flask setting
app = flask.Flask(__name__)

# Flask restful setting
api = Api(app)


app.config["DEBUG"] = True # Able to reload flask without exit the process
app.config["JWT_SECRET_KEY"] = "secret_key" #JWT token setting 

security_definitions = {
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

# SQLAlchemy setting
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{userName}:{userPassword}@{IPAddress}:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_timeout': 300,
}

# Swagger setting
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        securityDefinitions=security_definitions, # Able to add Jwt token in header in Swagger
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# URL(router)
api.add_resource(Users, "/users")
docs.register(Users)
api.add_resource(User, "/user/<int:id>")
docs.register(User)

api.add_resource(Orgs, "/organisation")
docs.register(Orgs)
api.add_resource(Org, "/organisation/<int:id>")
docs.register(Org)


if __name__ == '__main__':
    # JWT token setting
    jwt = JWTManager().init_app(app)

    db.init_app(app)
    db.app = app
    app.run(host='127.0.0.1', port=10009)