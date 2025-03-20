from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import requests
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

app.secret_key = '0ksklf8rfsks'

ALPHA_VANTAGE_API_KEY = "E675UAFI5MNUFS9A"
NEWS_API_KEY = "37bc020a6e544a2d8c9468f37c2081c7"


nltk.download('vader_lexicon')

@app.route("/success")
def success():
    flash("Your operation was successful!", "success")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")

# Display stock history page
@app.route("/stock_history", methods=["GET"])
def stock_history():
    return  render_template("stock_history.html")

# Display stock price page
@app.route("/stock_price", methods=["GET"])
def stock_price():
    return render_template("stock_price.html")

# Sentiment Analysis on Stock News
@app.route("/sentiment_analysis", methods=["GET"])
def sentiment_analysis():
    return render_template("sentiment_analysis.html")

# Stock Recommendation (Buy, Sell, Hold)
@app.route("/stock_recommendation", methods=["GET"])
def stock_recommendation():
    return render_template("stock_recommendation.html")

# Get stock detail data
@app.route("/get_stock_data", methods=["POST"])
def get_stock_data():
    try:
        symbol = request.json.get("symbol")
        if not symbol:
            flash("Stock symbol is required", "error")
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
        flash("Error: " + str(e), 'error')
        return jsonify({"error": str(e)}), 500

# Fetch stock history using Yahoo Finance for last month
@app.route("/stock_history/<symbol>", methods=["GET"])
def get_stock_history(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")

        # Convert index (dates) to strings
        hist.index = hist.index.strftime("%Y-%m-%d")

        # Convert DataFrame to dictionary
        data = hist.to_dict()

        return jsonify({"symbol": symbol, "history": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Fetch stock price using Alpha Vantage
@app.route("/stock_price/<symbol>", methods=["GET"])
def get_stock_price(symbol):
    try:
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format="pandas")
        data, _ = ts.get_quote_endpoint(symbol=symbol)
        return jsonify(data.to_dict(orient="records")[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Fetch news articles from Yahoo Finance
def get_stock_news(symbol):
    stock = yf.Ticker(symbol)
    news = stock.news  # Fetch recent news articles
    return news[:5] if news else []  # Limit to 5 articles

@app.route("/stock_news/<symbol>", methods=["GET"])
def get_stock_news_endpoint(symbol):
    news_articles = get_stock_news(symbol)
    if not news_articles:
        return jsonify({"error": "No news found for this stock"}), 404
    return jsonify(news_articles)

# Perform sentiment analysis on news headlines
def analayze_news(news_articles):
    sentiment_results = []
    for article in news_articles:
        headline = article['content'].get("title", "No title available")
        sentiment_score = sia.polarity_scores(headline)["compound"]
        sentiment_results.append({"headline": headline, "sentiment": sentiment_score})
    return sentiment_results


def sentiment_analysis_for(symbol):
    news_articles = get_stock_news(symbol)

    if not news_articles:
        return jsonify({"error": "No news found for this stock"}), 404

    sentiment_results = analayze_news(news_articles)
    
    # Calculate average sentiment score
    avg_sentiment = sum([item["sentiment"] for item in sentiment_results]) / len(sentiment_results)

    return {
        "symbol": symbol,
        "average_sentiment": avg_sentiment,
        "sentiment_details": sentiment_results
    }


@app.route("/sentiment_analysis/<symbol>", methods=["GET"])
def make_sentiment_analysis(symbol):
    return jsonify(sentiment_analysis_for(symbol))

# Stock Recommendation (Buy, Sell, Hold)
@app.route("/recommendation/<symbol>", methods=["GET"])
def stock_recommendation_for(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")["Close"]
        if len(hist) < 2:
            return jsonify({"error": "Not enough data"}), 400
        
        latest_close = hist.iloc[-1]
        previous_close = hist.iloc[-2]
        change = (latest_close - previous_close) / previous_close

        sentiment_resp = sentiment_analysis_for(symbol)
        sentiment = sentiment_resp["average_sentiment"]

        if change > 0.02 and sentiment > 0.2:
            recommendation = "Buy"
        elif change < -0.02 and sentiment < -0.2:
            recommendation = "Sell"
        else:
            recommendation = "Hold"

        return jsonify({"symbol": symbol, "recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

