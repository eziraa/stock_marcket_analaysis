import { showFlashMessage } from "./flash_messages.js";
export function fetchSentimentData() {
    const symbol = document.getElementById('symbolInput').value;
    const resultBox = document.getElementById('result');
    const stockSymbol = document.getElementById('stockSymbol');
    const sentimentList = document.getElementById('sentimentList');
    const averageSentiment = document.getElementById('averageSentiment');

    if (!symbol) {
        showFlashMessage('Please enter a stock symbol.', 'error');
        return;
    }
    // Clear previous result if any
    resultBox.classList.add('hidden');
    sentimentList.innerHTML = '';
    averageSentiment.textContent = '';

    const fetchSentimentButton = document.getElementById('fetchSentimentButton');
    fetchSentimentButton.disabled = true;
    fetchSentimentButton.innerText = 'Fetching...';

    fetch(`/sentiment_analysis/${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Show the results
            stockSymbol.textContent = symbol;
            averageSentiment.textContent = data.average_sentiment.charAt(0).toUpperCase() + data.average_sentiment.slice(1);

            data.sentiment_details.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.title;

                // Add color based on sentiment
                if (item.sentiment === 'positive') {
                    li.classList.add('positive');
                } else if (item.sentiment === 'negative') {
                    li.classList.add('negative');
                } else {
                    li.classList.add('neutral');
                }

                sentimentList.appendChild(li);
            });

            // Show the result box
            resultBox.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            showFlashMessage('Error fetching data: ' + error.message, 'error');
        }).finally(() => {
            fetchSentimentButton.disabled = false;
            fetchSentimentButton.innerText = 'Fetch';
        });
}

document.getElementById('fetchSentimentButton').addEventListener('click', fetchSentimentData);
