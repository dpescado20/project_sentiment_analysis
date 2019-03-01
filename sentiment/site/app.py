from sentiment.api.services_twitter import TwitterStreamer
from sentiment.api.classifier import Classifier

import os
import time
import json
import pandas as pd

cla = Classifier()
model = cla.load_model()
streamer = TwitterStreamer()
tweet = streamer.stream_tweets(['cancer'])

tweets_data_path = './social_media/tweets_data.txt'

os.remove(tweets_data_path)
time.sleep(1)
while not os.path.isfile(tweets_data_path):
    print('waiting for tweet_file_data')
    time.sleep(1)

while True:
    df = pd.DataFrame(columns=['tweet_id', 'sentiment'])
    tweets_data = []
    tweets_file = open(tweets_data_path, 'r')
    for line in tweets_file:
        if line.strip():
            tweets_data.append(json.loads(line))
    for tweet in tweets_data:
        df = df.append({
            'tweet_id': tweet['id'], 'sentiment': cla.sentiment(model, tweet['text'])['max']},
            ignore_index=True)
    df_pos = df[df['sentiment'] == 'pos'].count()
    df_neg = df[df['sentiment'] == 'neg'].count()
    data = [df_pos[0], df_neg[0]]
    print(data)
    time.sleep(5)
