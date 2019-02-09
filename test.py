from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from apps import credentials as crd


class StdOutListener(StreamListener):
    def on_data(self, raw_data):
        print(raw_data)
        return True

    def on_error(self, status_code):
        print(status_code)


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(crd.TW_CONSUMER_KEY, crd.TW_CONSUMER_SECRET)
    auth.set_access_token(crd.TW_ACCESS_TOKEN, crd.TW_ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(track=['donald trump'])
