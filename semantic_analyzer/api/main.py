from typing import List

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from .ml.model import Model, get_model
 
app = FastAPI()
 
 
class FindArticlesRequest(BaseModel):
    query: str
 
 
class FindArticlesResponse(BaseModel): 
    Headlines: List[str]
 
 
@app.post("/predict", response_model=FindArticlesResponse)
def predict(request: FindArticlesRequest, model: Model = Depends(get_model)):
    Headlines = model.predict(request.query)
    return FindArticlesResponse(
        Headlines=Headlines
    )