from transformers import pipeline

pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def sentiment_analysis(headline): # Uses pre-tuned model and returns whether it is "positive" or "negative"
    result = pipe(headline)
    return result[0]['label']
   