import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sentiment.nlp.cleaners import Cleaners

import pandas as pd
import numpy as np

cleaners = Cleaners()

print('LOADING VOCABULARY')
with open('./sentiment/nlp/vocabulary', 'rb') as model_vocab:
    vocabulary = pickle.load(model_vocab)

print('LOADING PRE TRAINED MODEL')
with open('./sentiment/nlp/model', 'rb') as model_clf:
    model = pickle.load(model_clf)
print('MODEL SUCCESSFULLY LOADED')

vectorizer = CountVectorizer(vocabulary=vocabulary)


class DataProcess:
    def get_cleaned_tweet(self, text):
        result = ' '.join(cleaners.spacy_tokenizer(text))
        return result

    def get_sentiment_score(self, text):
        text_vect = vectorizer.transform(cleaners.spacy_tokenizer(text))
        score = np.average(model.predict(text_vect))
        score = round(score, 4)
        return score

    def twitter_convert_searchResult_df(self, query):
        from sentiment.api.services_twitter import TwitterClient
        from urllib.parse import quote
        api = TwitterClient().get_twitter_client_api()
        data = []
        for result in api.search(q=quote(query), lang='en', result_type='mixed', count=100):
            data.append((result.created_at, result.text,))
        df = pd.DataFrame(columns=['Created_At', 'Tweet'], data=data)
        df['Tweet_Cleaned'] = [self.get_cleaned_tweet(tweet) for tweet in df.Tweet]
        df['Length_CT'] = [len(tweet) for tweet in df.Tweet_Cleaned]
        df = df[df.Length_CT > 2]
        df['Score'] = [self.get_sentiment_score(tweet) for tweet in df.Tweet]
        return df

    def youtube_convert_searchResult_df(self, query):
        from sentiment.api.services_youtube import YoutubeClient
        yt = YoutubeClient()
        data = yt.get_youtube_comments(query.lower())
        df = pd.DataFrame(columns=['Created_At', 'Tweet'], data=data)
        df['Tweet_Cleaned'] = [self.get_cleaned_tweet(tweet) for tweet in df.Tweet]
        df['Length_CT'] = [len(tweet) for tweet in df.Tweet_Cleaned]
        df = df[df.Length_CT > 2]
        df['Score'] = [self.get_sentiment_score(tweet) for tweet in df.Tweet]
        return df

    def facebook_convert_searchResult_df(self, query):
        from sentiment.api.services_facebook import FacebookClient
        fb = FacebookClient()
        data = fb.get_fb_post(query)
        df = pd.DataFrame(columns=['Created_At', 'Tweet', 'Like'], data=data)
        df['Tweet_Cleaned'] = [self.get_cleaned_tweet(tweet) for tweet in df.Tweet]
        df['Love'] = None
        df['Haha'] = None
        df['Angry'] = None
        df['Wow'] = None
        df['Sad'] = None
        return df


class DataResult:
    def __init__(self, df_query_function):
        self.df = df_query_function

    def get_df_row_count(self):
        df_len = self.df.shape
        row_count = df_len[0]
        return row_count

    def get_df_positive_score(self):
        df_pos = self.df.Score[self.df.Score > 0].count()
        return df_pos

    def get_df_negative_score(self):
        df_neg = self.df.Score[self.df.Score < 0].count()
        return df_neg

    def get_df_likes_sum(self):
        df_likes = self.df.Like.sum()
        return df_likes

    def get_df_original_tweet(self):
        tweet = self.df[['Created_At', 'Tweet', 'Score']]
        tweet.sort_values(by='Created_At', ascending=False, inplace=True)
        return tweet

    def get_df_original_post(self):
        post = self.df[['Created_At', 'Tweet', 'Like', 'Love', 'Haha', 'Angry', 'Wow', 'Sad']]
        post.rename(columns={'Tweet': 'Post', 'Created_At': 'Publish Date'}, inplace=True)
        return post

    def get_df_features(self):
        vectorizer = CountVectorizer()
        bow = vectorizer.fit_transform(self.df.Tweet_Cleaned).toarray()
        feature_names = vectorizer.get_feature_names()
        df = pd.DataFrame(bow, columns=feature_names)
        df = df.sum()
        df = df.reset_index()
        df.rename(columns={'index': 'Word', 0: 'Count'}, inplace=True)
        df.sort_values(by='Count', ascending=False, inplace=True)
        return df.head(50)
