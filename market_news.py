from newsapi.newsapi_client import NewsApiClient # type: ignore
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize News API with  API key
newsapi = NewsApiClient(api_key='c4a9b558635840799e3a2cfd83e5c885')

# Load FinBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Function to perform sentiment analysis
def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    labels = ["negative", "neutral", "positive"]
    sentiment = labels[torch.argmax(probabilities).item()]
    return sentiment

def get_news_sentiment(company_name):
    """Fetches latest news headlines for a given company and analyzes sentiment using FinBERT."""

    # Fetch latest news articles

    
    top_headlinesall_articles = newsapi.get_everything(q='apple',
                                    from_param='2025-03-12',
                                    to='2025-03-19',
                                    language='en',
                                    sort_by='relevancy',
                                    page=1)
  
    # Extract top 7 headlines
      
    content_list = []
    count = 0
    for article in top_headlinesall_articles['articles']:
      if 'content' in article and count < 7:
        content_list.append(article['content'])
      count += 1
      
    if not content_list:
        print("No relevant news articles found.")
        return "Neutral"


    # Analyze sentiment for each article
    
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    for news_article in content_list:
        sentiment = get_sentiment(news_article)
        sentiment_counts[sentiment] += 1

    # Determine overall market sentiment
    if sentiment_counts["positive"] > sentiment_counts["negative"]:
        overall_sentiment = "Bullish (Positive)"
    elif sentiment_counts["negative"] > sentiment_counts["positive"]:
        overall_sentiment = "Bearish (Negative)"
    else:
        overall_sentiment = "Neutral"
        
    sentiment_counts = {
        "Positive Impacts" : sentiment_counts["positive"],
        "Negative Impacts" : sentiment_counts["negative"],
        "Neutral Impacts" : sentiment_counts["neutral"]
    }

    return overall_sentiment, sentiment_counts

