from flask import Flask

app = Flask(__name__)

from api.twitter.routes import app_twitter

app.register_blueprint(app_twitter, url_prefix='/api')
