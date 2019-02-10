from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from apps import credentials as crd

import pandas as pd
import numpy as np


# # # # TWITTER CLIENT # # # #
class TwitterClient():
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
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(crd.TW_CONSUMER_KEY, crd.TW_CONSUMER_SECRET)
        auth.set_access_token(crd.TW_ACCESS_TOKEN, crd.TW_ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs
            return False
        print(status)


class TwitterAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[(tweet.id,
                                 tweet.created_at,
                                 tweet.text,
                                 tweet.source,
                                 tweet.favorite_count,
                                 tweet.retweet_count) for tweet in tweets],
                          columns=['id', 'date', 'tweets', 'source', 'likes', 'retweets']
                          )
        return df


if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TwitterAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets1 = api.user_timeline(screen_name='pbaconnect', count=20)
    tweets2 = api.user_timeline(screen_name='realDonaldTrump', count=20)

    df1 = tweet_analyzer.tweets_to_data_frame(tweets1)
    df2 = tweet_analyzer.tweets_to_data_frame(tweets2)

    df3 = pd.concat([df1, df2])
    df3.reset_index(inplace=True)

    print(df3)

