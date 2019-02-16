from flask import Blueprint
from flask_restplus import Api, Resource
from .services_twitter import TwitterClient, TwitterAnalyser
from .services_youtube import YoutubeClient, YoutubeAnalyser

app_api = Blueprint('api', __name__)
api = Api(app=app_api)
ns_twitter = api.namespace('twitter', description='Twitter Sentiments')
ns_facebook = api.namespace('facebook', description='Facebook Sentiments')
ns_youtube = api.namespace('youtube', description='Youtube Sentiments')


# # # # YOUTUBE ROUTES # # # #
@ns_youtube.route('/sentiments/<string:title>/')
class YoutubeSentimentCount(Resource):
    def get(self, title):
        """
        Returns process sentiments of Youtube
        """
        client = YoutubeClient()
        comments = client.get_youtube_comments(video_title=title)
        analyser = YoutubeAnalyser(comments)
        score = analyser.tweet_analyser_scores()
        return score


# # # # FACEBOOK ROUTES # # # #
@ns_facebook.route('/sentiments/')
class FacebookSentiment(Resource):
    def get(self):
        """
        Returns process sentiments of Facebook
        """
        return {'fb': 'sentiments'}


# # # # TWITTER ROUTES # # # #
@ns_twitter.route('/sentiments/<string:topic>/<int:count>/')
class TweetsSentiment(Resource):
    def get(self, topic, count):
        """
        Returns process sentiments of Twitter Tweets by Topic
        """
        tw_client = TwitterClient()
        api = tw_client.get_twitter_client_api()
        tweets = api.search(q=topic, count=count)

        analyser = TwitterAnalyser(tweets)
        score = analyser.tweet_analyser_scores()
        return score


@ns_twitter.route('/sentiments/<string:topic>/<int:count>/<string:since>/<string:until>/')
class TweetsSentimentFiltered(Resource):
    def get(self, topic, count, since, until):
        """
        Returns process sentiments of Twitter Tweets by Topic and Date
        """
        tw_client = TwitterClient()
        api = tw_client.get_twitter_client_api()
        tweets = api.search(q=topic, count=count, since=since, until=until)

        analyser = TwitterAnalyser(tweets)
        score = analyser.tweet_analyser_scores()
        return score


@ns_twitter.route('/sentiments/<string:client>/<int:count>/')
class TweetsSentimentClient(Resource):
    def get(self, count, client):
        """
        Returns process sentiments of Twitter Tweets by Client
        """
        tw_client = TwitterClient()
        api = tw_client.get_twitter_client_api()
        tweets = api.user_timeline(screen_name=client, count=count)

        analyser = TwitterAnalyser(tweets)
        score = analyser.tweet_analyser_scores()
        return score
