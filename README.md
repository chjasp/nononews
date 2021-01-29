# No Noise News (NoNoNews)

## Idea
The NoNoNews-skill let's a user define a set of words that are representative of his/her interests. The app then draws upon the most recent headlines from the NYT News API to serve the headlines that are semantically closest to the defined set of words. Additionally, the order in which the headlines are communicated to the user can be set to positive -> negative vice versa. 

Given that a user is interested in the news that have the most relevance to his/her own life, as opposed to a society at large, NoNoNews can be considered a meaningful extension to the supply of existing news apps for voice assistants. The overwhelming majority of those do not offer an effective way to restrict the news served to anything beyond broad categories. 

## Models & Deployment 
The Keras model used for sentiment analysis as well as the word embeddings have been trained on a Dataset of >1.6m tagged Tweets (training notebook based on: https://www.kaggle.com/paoloripamonti/twitter-sentiment-analysis). Both models are rather leightweight and can therefore be deployed to 2 separate (free tier) AWS EC2 instances (thus the split semantic_analyzer, sentiment_analyzer). In addition to the little cost, the models' small size yields the benefit of fast inference: To answer a request, the process of computing the cosine similarity, extracting the headlines most similar to the query, ordering the headlines by sentiment and returning them to the user takes less than 2 seconds.

## Alexa-Interface & Examples 
Users are able to specify up to 5 topics and the order positive->negative/negative->positive.

## Possible improvements
* The NYT API restricts access to a rather small amount of headlines in the free tier. For the final skill it would certainly make sense to have access to >200 articles a day to fully take advantage of the concept of semantic-retrieval.
* Though working reasonably well in the prototype, the service's precision could certainly be significantly improved by moving from 30 embedding dimensions to >100.
