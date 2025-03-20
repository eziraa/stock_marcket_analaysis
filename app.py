from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import yfinance as yf
# from alpha_vantage.timeseries import TimeSeries
import requests
from textblob import TextBlob
# from google import genai
app = Flask(__name__)

app.secret_key = '0ksklf8rfsks'
# Alpha Vantage API Key (replace with your own)
ALPHA_VANTAGE_API_KEY = "E675UAFI5MNUFS9A"
NEWS_API_KEY = "37bc020a6e544a2d8c9468f37c2081c7"

@app.route("/success")
def success():
    flash("Your operation was successful!", "success")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")

# Fetch stock price using Alpha Vantage
@app.route("/fetch_stock", methods=["POST"])
def fetch_stock():
    try:
        symbol = request.json.get("symbol")
        if not symbol:
            flash("Stock symbol is required", "error")
            print("Stock symbol is required")
            return redirect(url_for("home"))

        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        hist.index = hist.index.strftime("%Y-%m-%d")

        latest_close = hist["Close"].iloc[-1] if len(hist) > 0 else "N/A"

        sentiment_url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
        response = requests.get(sentiment_url)
        news_data = response.json()

        sentiment_scores = [
            TextBlob(article["title"]).sentiment.polarity for article in news_data.get("articles", [])
        ]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

        recommendation = "Hold"
        if avg_sentiment > 0.2:
            recommendation = "Buy"
        elif avg_sentiment < -0.2:
            recommendation = "Sell"

        return jsonify({
            "symbol": symbol,
            "latest_close": latest_close,
            "average_sentiment": round(avg_sentiment, 2),
            "recommendation": recommendation
        })
    
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        flash("Error: " + str(e), 'error')
        return jsonify({"error": str(e)}), 500

