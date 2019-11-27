from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import time

TW_CONSUMER_KEY = 'JauYlvETfEHaBmyJhVpHeY2k8'
TW_CONSUMER_SECRET = '0sU7tQiNfBb5lm8rDclXH78mDCNxJskaf4i0k9Q0XlsJoYGwxR'
TW_ACCESS_TOKEN = '1094173736129855488-5L8M2juPyAbalGjSE1GesU8paJRNBw'
TW_ACCESS_TOKEN_SECRET = 'mn8dIvJLu8fJ9a6DhTfq7YI85RDlKV0tDFrXvG6ttldUS'


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
        self.start_time = time.time()
        self.limit = 60

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            print(data)
            with open('./sentiment/api/stream_tweets.json', 'a') as tf:
                tf.write(data)
            return True
        else:
            print('DONE STREAMING')
            return False

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs
            return False
        print(status)
