from src.routes.flask_routes import *
from src.config.config import app_configs
from src.celery.celery_config import make_celery
from src.routes.flask_routes import users_api, users_api_get, login_api, verify_api


from flask import Flask
from flask_restful import Api

from flask_apispec.extension import FlaskApiSpec

# define flask app
app = Flask(__name__, template_folder='templates')
# define the restful api
api = Api(app)
# update the flask app to the selected config
app.config.update(app_configs.settings['flask'])
# create celery app
celery = make_celery(app)
celery.autodiscover_tasks(('src.twilio.otp',))
# generate swagger documentation
docs = FlaskApiSpec(app)

# define flask routes and link them to the api resource classes
api.add_resource(users_api, '/users')
api.add_resource(users_api_get, '/users/<string:user_id>')
api.add_resource(verify_api, '/verify')
api.add_resource(login_api, '/login')

# register swagger docs to each api resouce
docs.register(users_api)
docs.register(users_api_get)
docs.register(verify_api)

def main():
    app.run()


if __name__ == "__main__":
    main()
