from sentiment.api.services_twitter import TwitterStreamer

streamer = TwitterStreamer()
streamer.stream_tweets(['donald trump'])

from sentiment.nlp.classifier import Classifier

import json
import pandas as pd

cla = Classifier()

data = []
tweets = []
with open('./sentiment/api/stream_tweets.json', 'r') as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line))

print(len(data))
