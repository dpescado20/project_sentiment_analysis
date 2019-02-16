from flask import Flask

app = Flask(__name__)

from api.api_core.routes import app_api

app.register_blueprint(app_api, url_prefix='/api')


@app.route('/')
def index():
    return 'index view'
