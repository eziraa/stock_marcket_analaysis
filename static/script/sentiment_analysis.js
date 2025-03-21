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
                showFlashMessage(data.error, 'error');
                return;
            }
            else{
                showFlashMessage('Sentiment data fetched successfully.', 'success');
            }

            // Show the results
            console.log(data)
            stockSymbol.textContent = symbol;

            let sentimentText = 'Neutral'; // Default sentiment
            if (data.average_sentiment > 0) {
                sentimentText = 'Positive';
            } else if (data.average_sentiment < 0) {
                sentimentText = 'Negative';
            }
            averageSentiment.textContent = sentimentText;

            data.sentiment_details.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.headline;
                // Add color based on sentiment
                if (item.sentiment > 0) {
                    li.classList.add('positive');
                    li.style.color = 'green';
                } else if (item.sentiment < 0) {
                    li.classList.add('negative');
                    li.style.color = 'red';
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
