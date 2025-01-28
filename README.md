# Sentiment-Based Stock Trading Bot  

## Description  
This bot automates trading decisions by analyzing financial news headlines. Using a combination of web scraping, sentiment analysis, and real-time data APIs, it determines whether to buy or short stocks. The backend is built with Flask, while the React-based frontend visualizes portfolio performance and trade history. Automation is handled via GitHub Actions to ensure continuous updates.

---

## Image  
*(Need to add image)*

---

## Detailed Description  

### **1. Backend**  
- **News Scraping**: Headlines are scraped from **Yahoo Finance** using **Beautiful Soup**.  
- **Sentiment Analysis**: Headlines are analyzed with the NLP model **`mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis`** from Hugging Face to classify them as positive, neutral, or negative.  
- **Trade Execution**:  
  - Based of the sentiment it buys/shorts around $1000 of the stock
  - Real-time stock prices are fetched via **Finnhub's API**, ensuring accurate trade execution.  
- **Portfolio Management**: Tracks cash, active trades, trade history, and portfolio value over time.  

### **2. Frontend**  
- Built with **React** to visualize portfolio performance and trade history.  
- Uses **Chart.js** to display a real-time graph of portfolio value.  
- Includes tables for active and historical trades, providing clear insights into trading activity.  

### **3. Automation**  
- **GitHub Actions** handles scheduled updates, ensuring that trades, portfolio logs, and stock prices are refreshed automatically without manual intervention.  

---

## References  
- **Hugging Face NLP**: Sentiment analysis powered by the fine-tuned model `mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis`.  
