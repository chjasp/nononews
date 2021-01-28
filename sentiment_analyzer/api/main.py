# coding: utf8
import uvicorn
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from api.ml.model import Model


app = FastAPI()


# Handle GET-requests (output: Dummy-response)#

@app.get("/")
def main_response():
	return {"message" : "Post to /predict for predictions."}


# Handle POST-requests (output: String-list, sorted by sentiment)

model = Model()
model.load()

class Articles(BaseModel):
	headlines : List[str]
	order     : int 

@app.post("/predict")
def predict(articles: Articles):
	ordered_articles = model.compute_scores(articles.headlines, articles.order)
	return {"ordered_articles" : ordered_articles}

"""
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
"""
