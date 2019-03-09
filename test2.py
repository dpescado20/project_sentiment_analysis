# from sentiment.api.services_twitter import TwitterStreamer

# streamer = TwitterStreamer()
# streamer.stream_tweets(['donald trump'])

import json
import pandas as pd

from sentiment.nlp.classifier import Classifier

cla = Classifier()
model = cla.load_model()

data = []
tweets = []
with open('./sentiment/api/stream_tweets.json', 'r') as stream_tweets:
    for line in stream_tweets:
        if line.strip():
            data.append(json.loads(line))
for tweet in data:
    score = cla.sentiment(model, tweet['text'])
    if score['max'] == 'pos':
        polarity = score['pos']
    else:
        polarity = score['neg'] * -1

    tweets.append((tweet['created_at'],
                   tweet['text'],
                   polarity))

df = pd.DataFrame(columns=['created_at', 'tweet', 'polarity'], data=tweets)

print(df.head())
