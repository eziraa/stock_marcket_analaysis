import { showFlashMessage } from "./flash_messages.js";

export function fetchRecommendation() {
    const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
    if (!symbol) {
        showFlashMessage("Please enter a stock symbol.", 'error');
        return;
    }

    const recommendationButton = document.getElementById("getRecommendationBtn");
    recommendationButton.disabled = true;
    recommendationButton.innerText = "Fetching...";

    fetch(`/recommendation/${symbol}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showFlashMessage(data.error, 'error');
            return;
        }
        else{
            showFlashMessage("Stock recommendation fetched successfully.", 'success');
        }

        document.getElementById("stockSymbol").innerText = symbol;
        document.getElementById("recommendation").innerText = data.recommendation;

        document.getElementById("result").classList.remove("hidden");
    })
    .catch(error => {
        console.error("Error fetching stock recommendation:", error);
        showFlashMessage("An error occurred while fetching stock recommendation", 'error');
    }).finally(() => {
        recommendationButton.disabled = false;
        recommendationButton.innerText = "Get Recommendation";
    });
}

document.getElementById("getRecommendationBtn").addEventListener("click", fetchRecommendation);
// The fetchRecommendation function is similar to fetchStockData, but it fetches stock recommendation data instead of stock history data.
