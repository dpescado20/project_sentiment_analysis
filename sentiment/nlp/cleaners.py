import re
import string

import emoji
import en_core_web_sm
from bs4 import BeautifulSoup
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from textacy import preprocess
import ftfy


class Cleaners:
    def __init__(self):
        # EMOTICONS
        self.SMILEY = {
            "^-^": "happy",
            ":‑)": "happy",
            ":-]": "happy",
            ":-3": "happy",
            ":->": "happy",
            "8-)": "happy",
            ":-}": "happy",
            ":)": "happy",
            ":]": "happy",
            ":3": "happy",
            ":>": "happy",
            "8)": "happy",
            ":}": "happy",
            ":o)": "happy",
            ":c)": "happy",
            ":^)": "happy",
            "=]": "happy",
            "=)": "happy",
            ":-))": "happy",
            ":‑D": "happy",
            "8‑D": "happy",
            "x‑D": "happy",
            "X‑D": "happy",
            ":D": "happy",
            "8D": "happy",
            "xD": "happy",
            "XD": "happy",
            ":‑(": "sad",
            ":‑c": "sad",
            ":‑<": "sad",
            ":‑[": "sad",
            ":(": "sad",
            ":c": "sad",
            ":<": "sad",
            ":[": "sad",
            ":-||": "sad",
            ">:[": "sad",
            ":{": "sad",
            ":@": "sad",
            ">:(": "sad",
            ":'‑(": "sad",
            ":'(": "sad",
            ":‑P": "playful",
            "X‑P": "playful",
            "x‑p": "playful",
            ":‑p": "playful",
            ":‑Þ": "playful",
            ":‑þ": "playful",
            ":‑b": "playful",
            ":P": "playful",
            "XP": "playful",
            "xp": "playful",
            ":p": "playful",
            ":Þ": "playful",
            ":þ": "playful",
            ":b": "playful",
            "<3": "love"
        }

        # SPACY INITIALIZATION
        # self.nlp = spacy.load('en_core_web_sm')
        self.nlp = en_core_web_sm.load()
        self.stopwords = list(STOP_WORDS)
        self.punctuations = string.punctuation
        self.parser = English()

    # CLEAN TEXT
    def clean_tweet(self, text):
        # FIXED UNICODE
        # text = preprocess.fix_bad_unicode(text)
        text = ftfy.fix_text(text)

        # GET TEXT ONLY FROM HTML
        text = BeautifulSoup(text, features='lxml').getText()
        # UN-PACK CONTRACTIONS
        text = preprocess.unpack_contractions(text)

        # REMOVE URL
        text = preprocess.replace_urls(text)

        # REMOVE EMAILS
        text = preprocess.replace_emails(text)

        # REMOVE PHONE NUMBERS
        text = preprocess.replace_phone_numbers(text)

        # REMOVE NUMBERS
        text = preprocess.replace_numbers(text)

        # REMOVE CURRENCY
        text = preprocess.replace_currency_symbols(text)

        # REMOVE ACCENTS
        text = preprocess.remove_accents(text)

        # CONVERT EMOJIS TO TEXT
        words = text.split()
        reformed = [self.SMILEY[word] if word in self.SMILEY else word for word in words]
        text = " ".join(reformed)
        text = emoji.demojize(text)
        text = text.replace(":", " ")
        text = ' '.join(text.split())

        # SPLIT ATTACHED WORDS
        text = ' '.join(re.findall('[A-Z][^A-Z]*', text))

        # SPLIT UNDERSCORE WORDS
        text = text.replace('_', ' ')

        # REMOVE PUNCTUATION
        text = preprocess.remove_punct(text)

        # Remove numbers
        text = re.sub(r'\d', '', text)

        # REMOVE WORDS LESS THAN 3 CHARACTERS
        text = re.sub(r'\b\w{1,2}\b', '', text)

        # NORMALIZE WHITESPACE
        text = preprocess.normalize_whitespace(text)

        return text

    # SPACY TOKENIZER
    def spacy_tokenizer(self, text):
        tokens = self.parser(self.clean_tweet(text))
        tokens = [word.lemma_.lower().strip() if word.lemma_ != '-PRON-' else word.lower_ for word in tokens]
        tokens = [word for word in tokens if
                  word not in self.stopwords and word not in self.punctuations and word.isdigit() == False]
        return tokens
