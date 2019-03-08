import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Event
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import pandas as pd
from datetime import datetime
import json
import os
import time
from textblob import TextBlob
from collections import deque
import arrow
import random

from sentiment import dashapp
from sentiment.site import dash_components as dac
from sentiment.nlp.classifier import Classifier
from sentiment.api.services_twitter import TwitterStreamer

streamer = TwitterStreamer()
tweet = streamer.stream_tweets(['donald trump'])

cla = Classifier()
model = cla.load_model()

tweets_data_path = './sentiment/api/stream_tweets.json'
tweets_process_path = './sentiment/api/process_tweets.json'

if os.path.isfile(tweets_data_path) is True:
    os.remove(tweets_data_path)
    time.sleep(1)

while not os.path.isfile(tweets_data_path):
    print('waiting for tweet_file_data')
    time.sleep(1)

dashapp.layout = html.Div(
    [
        dac.navbar,
        html.Br(),
        dac.create_body(
            [
                dac.create_card_main(
                    title='Twitter Sentiments Score',
                    content=[
                        dbc.Col([
                            dcc.Graph(id='tw-sent-graph', animate=True),
                            dcc.Interval(
                                id='tw-sent-graph-update',
                                interval=1 * 1000)
                        ])
                    ]
                ),
                html.Br(),
                dac.create_card_main(
                    title='Facebook Sentiments Score',
                    content=[
                        dbc.Col(
                            dac.create_card_main(title='graph area', content=None),
                        ),
                        dbc.Col(
                            dac.create_card_main(title='explanation', content=None),
                        )
                    ]
                ),
                html.Br(),
                dac.create_card_main(
                    title='Youtube Sentiments Score',
                    content=[
                        dbc.Col(
                            dac.create_card_main(title='graph area', content=None),
                        ),
                        dbc.Col(
                            dac.create_card_main(title='explanation', content=None),
                        )
                    ]
                )
            ]
        )
    ]
)


@dashapp.callback(Output('tw-sent-graph', 'figure'),
                  events=[Event('tw-sent-graph-update', 'interval')])
def tw_graph_update():
    with open(tweets_data_path, 'r') as tweets_file:
        tweet_data = []
        data = []
        for line in tweets_file:
            if line.strip():
                tweet_data.append(json.loads(line))
        for tweet in tweet_data:
            data.append((datetime.strftime(
                datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
                '%Y-%m-%d %H:%M'),  # '%Y-%m-%d %H:%M:%S'
                         cla.sentiment(model, tweet['text'])['pos'] * 100.00,
                         cla.sentiment(model, tweet['text'])['neg'] * 100.00))

        df = pd.DataFrame(columns=['created_at', 'pos', 'neg'], data=data)
        # df1 = df.tail(100)
        df['timezone_created'] = pd.to_datetime(df['created_at'])
        df['created_attz'] = df['timezone_created'] + pd.Timedelta(hours=8)
        df = df.groupby(['created_attz']).mean()
        df.reset_index(inplace=True)
    data = (
        [
            go.Scatter(
                x=list(df['created_attz']),
                y=list(df['pos']),
                name='Positive',
                mode='lines+markers'
            ),
            go.Scatter(
                x=list(df['created_attz']),
                y=list(df['neg']),
                name='Negative',
                mode='lines+markers'
            )
        ]
    )
    layout = go.Layout(
        showlegend=True,
        # margin=go.layout.Margin(l=40, r=0, t=40, b=30),
    )
    return {'data': data, 'layout': layout}
