# coding: utf8
import keras
import fastapi
import pandas

from keras.models import load_model 
from keras.preprocessing.text import Tokenizer 
from keras.preprocessing.sequence import pad_sequences 

from gensim.models import Word2Vec 
import pickle 


class Model:

    def __init__(self):
        self.SEQUENCE_LENGTH = 300

        self.w2v_model       = None 
        self.model           = None 
        self.tokenizer       = None


    def load(self):
        self.w2v_model       = Word2Vec.load("./api/ml/models/model.w2v") 
        self.model           = load_model("./api/ml/models/model.h5") 
        with open("./api/ml/models/tokenizer.pkl", 'rb') as fd: 
            self.tokenizer   = pickle.load(fd)


    def order_articles(self, articles, scores, order):
        ordered_articles = [None for le in range(len(articles))]

        if (order == 1):
            for i in range(len(articles)):
                ind = scores.index(max(scores))
                ordered_articles[i] = articles[ind]
                scores[ind] = -100

        else:
            for i in range(len(articles)):
                print("i")
                ind = scores.index(min(scores))
                ordered_articles[i] = articles[ind]
                scores[ind] = 100
        
        return ordered_articles
    	

    def compute_scores(self, articles, order): 
        sentiment_scores = [None for le in range(len(articles))] 

        for i in range(len(articles)):
            preprocessed_article = pad_sequences(self.tokenizer.texts_to_sequences([articles[i]]), maxlen=self.SEQUENCE_LENGTH)
            sentiment_scores[i] = self.model.predict([preprocessed_article])[0]

        ordered_articles = self.order_articles(articles, sentiment_scores, order)

        return ordered_articles 
