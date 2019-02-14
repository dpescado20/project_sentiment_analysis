from flask import Blueprint
from flask_restplus import Api, Resource

app_twitter = Blueprint('twitter', __name__)
api_twitter = Api(app=app_twitter)
ns_twitter = api_twitter.namespace('twitter', description='Twitter Sentiments')


@ns_twitter.route('/tweets/<int:count>/')
class TwitterTweetsClient(Resource):
    def get(self, count):
        """
        Returns process sentiments of Twitter tweets
        """
        return {'count': count}


@ns_twitter.route('/tweets/<int:count>/<string:client>/')
class TwitterTweetsClient(Resource):
    def get(self, count, client):
        """
        Returns process sentiments of Twitter Client tweets
        """
        return 'client tweets'
