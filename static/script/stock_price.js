import { showFlashMessage } from "./flash_messages.js";

export function fetchStockPrice() {
    const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
    if (!symbol) {
        showFlashMessage("Please enter a stock symbol.", "error");
        return;
    }

    const fetchStockPriceButton = document.getElementById("fetchStockPriceButton");
    fetchStockPriceButton.disabled = true;
    fetchStockPriceButton.innerText = "Fetching...";
    fetch(`/stock_price/${symbol}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showFlashMessage(data.error, "error");
            return;
        }
        else{
            showFlashMessage("Stock data fetched successfully.", "success");
        }

        document.getElementById("stockSymbol").innerText = symbol;
        document.getElementById("stockPrice").innerText = parseFloat(data["05. price"]).toFixed(2);
        document.getElementById("stockHigh").innerText = parseFloat(data["03. high"]).toFixed(2);
        document.getElementById("stockLow").innerText = parseFloat(data["04. low"]).toFixed(2);
        document.getElementById("stockVolume").innerText = data["06. volume"];
        document.getElementById("result").classList.remove("hidden");
    })
    .catch(error => {
        console.error("Error:", error);
        showFlashMessage("An error occurred while fetching stock data.", "error");
    }).finally(() => {
        fetchStockPriceButton.disabled = false;
        fetchStockPriceButton.innerText = "Fetch";
    });
}

document.getElementById("fetchStockPriceButton").addEventListener("click", fetchStockPrice);
// This script fetches the latest stock price data from the Alpha Vantage API using the /stock_price/<symbol> route. The response data includes the latest price, high, low, and volume for the specified stock symbol. The data is displayed on the page, and an error message is displayed if the symbol is invalid or if there is an error fetching the data.