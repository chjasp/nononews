import requests 
import numpy as np
import heapq
from gensim.models import KeyedVectors
 

class Model:
    def __init__(self):
 
        self.model = Word2Vec.load("./api/ml/models/model.w2v")

    def predict(self, query):
        # Get most viewed articles for the last seven days:
        url = 'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=XQGPC5b5IGcYrgSi0tm4bMNPkRurGOaO' 
        # Make the request
        response = requests.get(url)
        response_json = response.json()

        sentence = []
        for i in response_json['results']:
            sentence.append(i['title'])

        num_top_related=3

        wmdis = []
        most_related_headline = []
        for headline in sentence:
            wmdis.append(self.model.wmdistance(query, headline))
        h = heapq.nsmallest(num_top_related, wmdis)
        idx = np.where(np.isin(wmdis,h))
        for i in range(num_top_related):
            most_related_headline.append(sentence[idx[0][i]])
            
        return (
            most_related_headline
        )
  
model = Model()

def get_model():
    return model