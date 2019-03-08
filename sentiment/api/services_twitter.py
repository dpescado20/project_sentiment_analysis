from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# from sentiment.nlp.classifier import Classifier
import pandas as pd
import json
from datetime import datetime
import time
import collections

TW_CONSUMER_KEY = 'HO0JFLVoiVfXuIDzIVoyrIlUL'
TW_CONSUMER_SECRET = 'Tnv4NI3LEwqnVmjSzCsNem2tTiH8ZrYscnmwN5Gmw2J30C2ZwV'
TW_ACCESS_TOKEN = '1094173736129855488-9n4qdUJkSvkNJOYA7SK8XQ12BIzYr7'
TW_ACCESS_TOKEN_SECRET = 'GfbyjzC9VxnXeJ12uKyKaC8vuglHwRSlh9ABmIxOEaeAu'


# cla = Classifier()
# model = cla.load_model()


# # # # TWITTER CLIENT # # # #
class TwitterClient:
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_twitter_client_api(self):
        return self.twitter_client


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator:
    def authenticate_twitter_app(self):
        auth = OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
        auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer:
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, hash_tag_list):  # fetched_tweets_filename,
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = TwitterListener()  # fetched_tweets_filename
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list, languages=['en,tl'], is_async=True)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self):  # fetched_tweets_filename
        super(TwitterListener).__init__()
        # self.fetched_tweets_filename = fetched_tweets_filename
        self.num_tweets = 0

    def on_data(self, data):
        if self.num_tweets < 100:
            with open('./sentiment/api/stream_tweets.json', 'a') as tf:
                tf.write(data)
            print(self.num_tweets)
            self.num_tweets += 1
            return True
        else:
            return False

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs
            return False
        print(status)


'''class TwitterAnalyzer:
    def __init__(self, tweets):
        self.tweets = tweets
        self.cla = Classifier()
        self.model = self.cla.load_model()

    def score(self):
        sentiment = self.cla.sentiment(self.model, self.tweets)
        return sentiment'''
