import requests
from transformers import pipeline

# Load the pre-trained DistilBERT model and tokenizer
# model_name = "distilbert-base-uncased"
# tokenizer = DistilBertTokenizer.from_pretrained(model_name)
# model = DistilBertForSequenceClassification.from_pretrained(model_name)

# Define the URL and API key
url = "https://newsapi.org/v2/everything"
api_key = "201fc85e2561451fb252dd74c07297e7"

def performSentimentalAnalysis(company_name = ''):
    # Define the parameters for the request
    params = {
        "q": '"' + company_name + '"',
        "apiKey": api_key,
        "searchIn": 'title',
        "pageSize": 15
    }

    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Perform sentiment analysis
        sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
        results = sentiment_analysis(list(map(lambda article: article['content'], data['articles'])))
        
        def formatObject(arg):
            (i, result) = arg
            article = data['articles'][i]
            
            title = article['title']
            description = article['description']
            content = article['content']

            return {
                "title": title,
                "url": data['articles'][i]['url'],
                "source": data['articles'][i]['source']['name'],
                "label": result['label'],
                "score": result['score']
            }

        return list(map(formatObject, enumerate(results)))
    else:
        # If the request was not successful, print an error message
        print("Error:", response.status_code)
        return []

if __name__ == "__main__":
    print("------------")
    data = performSentimentalAnalysis('Microsoft')
    print(data)