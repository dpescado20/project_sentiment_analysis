from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import twitter_samples, stopwords, movie_reviews
from nltk.metrics import precision, recall, f_measure, ConfusionMatrix

import re
import string
from random import shuffle
from collections import defaultdict

import pickle


class Classifier:
    def __init__(self):
        self.stemmer = WordNetLemmatizer()
        self.stopwords_english = stopwords.words('english')

        self.pos_tweets = twitter_samples.strings('positive_tweets.json')
        self.neg_tweets = twitter_samples.strings('negative_tweets.json')

        # Happy Emoticons
        emoticons_happy = ([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
        ])

        # Sad Emoticons
        emoticons_sad = ([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
        ])

        # all emoticons (happy + sad)
        self.emoticons = set(emoticons_happy).union(set(emoticons_sad))

    def clean_tweets(self, tweet):
        # remove stock market tickers like $GE
        tweet = re.sub(r'\$\w*', '', tweet)
        # remove old style retweet text "RT"
        tweet = re.sub(r'^RT[\s]+', '', tweet)
        # remove hyperlinks
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
        # remove the hash # sign from the word
        tweet = re.sub(r'#', '', tweet)

        # tokenize tweets
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        tweet_tokens = tokenizer.tokenize(tweet)

        tweets_clean = []
        for word in tweet_tokens:
            if (word not in self.stopwords_english and  # remove stopwords
                    word not in self.emoticons and  # remove emoticons
                    word not in string.punctuation):  # remove punctuation
                # tweets_clean.append(word)
                stem_word = self.stemmer.lemmatize(word)  # stemming word
                tweets_clean.append(stem_word)
        return tweets_clean

    # feature extractor function
    def bag_of_words(self, tweet):
        words = self.clean_tweets(tweet)
        words_dictionary = dict([word, True] for word in words)
        return words_dictionary

    def train_test_set(self, pos_tweets, neg_tweets):
        # positive tweets feature set
        pos_tweets_set = []
        for tweet in pos_tweets:
            pos_tweets_set.append((self.bag_of_words(tweet), 'pos'))

        # negative tweets feature set
        neg_tweets_set = []
        for tweet in neg_tweets:
            neg_tweets_set.append((self.bag_of_words(tweet), 'neg'))

        # randomize pos_reviews_set and neg_reviews_set
        # doing so will output different accuracy result everytime we run the program
        shuffle(pos_tweets_set)
        shuffle(neg_tweets_set)

        pos_count = int(len(pos_tweets) * 0.20)
        neg_count = int(len(neg_tweets) * 0.20)

        test_set = pos_tweets_set[:pos_count] + neg_tweets_set[:neg_count]
        train_set = pos_tweets_set[pos_count:] + neg_tweets_set[neg_count:]
        return {'test_set': test_set, 'train_set': train_set}

    def train_classifier(self, train_test_set):
        classifier = NaiveBayesClassifier.train(train_test_set['train_set'])
        # accuracy = classify.accuracy(classifier, train_test_set['test_set'])
        return classifier

    def metrics_classifier(self, classifier, test_set):
        # Precision, Recall & F1-Score
        actual_set = defaultdict(set)
        predicted_set = defaultdict(set)

        actual_set_cm = []
        predicted_set_cm = []

        for index, (feature, actual_label) in enumerate(test_set):
            actual_set[actual_label].add(index)
            actual_set_cm.append(actual_label)

            predicted_label = classifier.classify(feature)

            predicted_set[predicted_label].add(index)
            predicted_set_cm.append(predicted_label)

        pos_precision = precision(actual_set['pos'], predicted_set['pos'])
        pos_recall = recall(actual_set['pos'], predicted_set['pos'])
        pos_fmeasure = f_measure(actual_set['pos'], predicted_set['pos'])

        neg_precision = precision(actual_set['pos'], predicted_set['pos'])
        neg_recall = recall(actual_set['pos'], predicted_set['pos'])
        neg_fmeasure = f_measure(actual_set['pos'], predicted_set['pos'])

        cm = ConfusionMatrix(actual_set_cm, predicted_set_cm)
        # cm = cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9)
        return {'pos_precision': pos_precision, 'pos_recal': pos_recall, 'pos_fmeasure': pos_fmeasure,
                'neg_precision': neg_precision, 'neg_recall': neg_recall, 'neg_fmeasure': neg_fmeasure,
                'confusion_matrix': cm}

    # # # # SAVING THE MODEL # # # #
    def save_model(self, classifier):
        with open('./sentiment/nlp/text_classifier', 'wb') as picklefile:
            pickle.dump(classifier, picklefile)
        return print('model successfully saved')

    # # # # LOADING THE MODEL # # # #
    def load_model(self):
        with open('./sentiment/nlp/text_classifier', 'rb') as training_model:
            model = pickle.load(training_model)
            print('model successfully loaded')
        return model

    # # # # CUSTOM TWEET # # # #
    def sentiment(self, classifier, tweet):
        tweet_set = self.bag_of_words(tweet)
        prob_result = classifier.prob_classify(tweet_set)
        return {'max': prob_result.max(), 'pos': prob_result.prob('pos'), 'neg': prob_result.prob('neg')}
