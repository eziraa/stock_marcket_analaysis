from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import requests
from textblob import TextBlob
import google.generativeai as genai
app = Flask(__name__)

app.secret_key = '0ksklf8rfsks'
# Alpha Vantage API Key (replace with your own)
ALPHA_VANTAGE_API_KEY = "E675UAFI5MNUFS9A"
NEWS_API_KEY = "37bc020a6e544a2d8c9468f37c2081c7"

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyDy0yU4PzJtVZ14MMY3O6I00SkCJ7L69mY"


# Set up the API key
genai.configure(api_key=GEMINI_API_KEY)

# Example usage
model = genai.GenerativeModel("gemini-2.0-flash")


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

# Define the sentiment analysis function using Gemini AI
def analyze_sentiment_with_gemini(text):
    try:
        # Sending content to Gemini for sentiment analysis
        # response = client.models.generate_content(
        #     model="gemini-2.0-flash",  # Use the sentiment analysis model
        #     contents=text
        # )
        response = model.generate_content(text)


        # Extract the sentiment from the response (adjust according to Gemini's response structure)
        sentiment = response.text.strip()  # Adjust this based on Gemini's actual response format

        # Return the sentiment (Gemini should return 'positive', 'negative', 'neutral')
        return sentiment
    except Exception as e:
        print(f"Error during sentiment analysis: {str(e)}")
        return "neutral"  # Default sentiment if there's an error
# Endpoint to analyze sentiment of stock-related news articles
@app.route("/sentiment_analysis/<symbol>", methods=["GET"])
def make_sentiment_analysis(symbol):
    try:
        # Replace with your NewsAPI endpoint or any other news service API
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        news = response.json().get("articles", [])
        
        
        if not news:
            flash("No aricles found for the symbol", "error")
            return jsonify({"error": "No articles found for the symbol"}), 404

        sentiment_scores = []
        for article in news:
            title = article.get("title", "")
            description = article.get("description", "")
            content = article.get("content", "")

            text = title + " " + description + " " + content
            sentiment = analyze_sentiment_with_gemini(text)
            sentiment_scores.append({
                'title': article.get("title"),
                'sentiment': sentiment
            })
        
        avg_sentiment = 'neutral'  # Default if no valid sentiment score
        if sentiment_scores:
            sentiment_count = {"positive": 0, "neutral": 0, "negative": 0}
            for score in sentiment_scores:
                sentiment_count[score['sentiment']] += 1

            # Determine overall sentiment (majority rule)
            avg_sentiment = max(sentiment_count, key=sentiment_count.get)

        return jsonify({"symbol": symbol, "average_sentiment": avg_sentiment, "sentiment_details": sentiment_scores})
    
    except Exception as e:
        print(f"Error during sentiment analysis: {str(e)}")
        flash ("Error: " + str(e), "error")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

