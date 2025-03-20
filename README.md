# 📊 Stock Sentiment Analysis API

## 🚀 Overview
This API provides **real-time sentiment analysis** for stock market news related to a given stock symbol (e.g., AAPL, GOOGL, TSLA). It fetches financial news, analyzes sentiment, and returns insights to help investors make data-driven decisions.

## 🏗️ Features
- 🔍 **Real-time News Fetching** – Retrieves the latest financial news articles.
- 🧠 **Sentiment Analysis** – Classifies news as **Positive, Negative, or Neutral**.
- 📈 **Stock Insights** – Helps investors gauge market sentiment.
- ⚡ **Fast & Scalable** – Built using Flask and Gunicorn.

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Data Processing:** Pandas, NLTK (or Google Gemini for AI-based sentiment)
- **API Hosting:** Render / Heroku
- **Database (if needed):** PostgreSQL

## 📌 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/eziraa/stock_sentiment_analysis.git
cd stock-sentiment-analysis
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file and add the necessary API keys:
```
NEWS_API_KEY=your_news_api_key
GOOGLE_GEMINI_API_KEY=your_google_gemini_key  # If using Google AI
```

### 4️⃣ Run the Application
```bash
python app.py  # OR
flask run
```

The API will be available at: `http://127.0.0.1:5000/`

## 🔥 API Endpoints

### 1️⃣ Get Sentiment for a Stock Symbol
**Endpoint:**
```http
GET /sentiment/{stock_symbol}
```
**Example Request:**
```http
GET /sentiment/GOOGL
```
**Response:**
```json
{
  "stock": "GOOGL",
  "average_sentiment": "Positive",
  "news": [
    {
      "title": "Google expands AI research in Europe",
      "sentiment": "Positive"
    },
    {
      "title": "EU fines Google for antitrust violations",
      "sentiment": "Negative"
    }
  ]
}
```
### Deployement

[See](https://stock-marcket-analaysis.onrender.com)


## 📜 License
MIT License

## 🤝 Contributing
Pull requests are welcome! Open an issue for bug fixes or feature requests.

## 📬 Contact
- GitHub: [YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com

