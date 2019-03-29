from nltk.corpus import twitter_samples

import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from sentiment.nlp.cleaners import spacy_tokenizer

# NLTK CORPUS
pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings('negative_tweets.json')

# MACHINE LEARNING
data = []
for word in pos_tweets:
    data.append((' '.join(spacy_tokenizer(word)), 1))
for word in neg_tweets:
    data.append((' '.join(spacy_tokenizer(word)), -1))
df = pd.DataFrame(columns=['tweet', 'label'], data=data)

X = df.tweet
y = df.label

# TT SPLIT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# VECTORIZE
vect = CountVectorizer(max_features=1000, binary=True)
X_train_vect = vect.fit_transform(X_train)

print('saving vocabulary')
with open('.sentiment/nlp/vocabulary', 'wb') as picklevocab:
    pickle.dump(vect.vocabulary_, picklevocab)
print('vocabulary saved')

# TRAIN MODEL
model = MultinomialNB()
model.fit(X_train_vect, y_train)
score = model.score(X_train_vect, y_train)

# EVALUATE MODEL
X_test_vect = vect.transform(X_test)
y_pred = model.predict(X_test_vect)

# print('Accuracy: {}'.format(accuracy_score(y_test, y_pred)))
# print('F1 Score: {}'.format(f1_score(y_test, y_pred)))
# print('Report: \n', classification_report(y_test, y_pred))
# print('Confusion Matrix: \n', confusion_matrix(y_test, y_pred))

print('saving model')
with open('.sentiment/nlp/model', 'wb') as picklemodel:
    pickle.dump(model, picklemodel)
print('model saved')
