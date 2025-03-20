import { showFlashMessage } from "./flash_messages.js"; 

 export function fetchStockData() {
    const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
    if (!symbol) {
        showFlashMessage("Please enter a stock symbol.", "error");
        return;
    }

    fetch("/fetch_stock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol: symbol })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("stockSymbol").innerText = data.symbol;
        document.getElementById("stockPrice").innerText = data.latest_close;
        document.getElementById("sentiment").innerText = data.average_sentiment;
        document.getElementById("recommendation").innerText = data.recommendation;

        document.getElementById("result").classList.remove("hidden");
    })
    .catch(error => console.error("Error fetching stock data:", error));
}

document.getElementById("fetchButton").addEventListener("click", fetchStockData);