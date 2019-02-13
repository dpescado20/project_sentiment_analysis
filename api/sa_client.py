from flask import Flask
from flask_restful import Api, Resource

import api.twitter_backend as tb

app = Flask(__name__)
api = Api(app)


class TwitterSentiments(Resource):
    def get(self, name, count):
        client = tb.TwitterClient.get_twitter_client_api()
        return 'hellow'


api.add_resource(TwitterSentiments, '/rest/twitter/client/{<string:name>,<int:count>')

app.run(debug=True)
