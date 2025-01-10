from transformers import pipeline

pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def sentiment_analysis(headline):
    result = pipe(headline)
    return result[0]['label']
   