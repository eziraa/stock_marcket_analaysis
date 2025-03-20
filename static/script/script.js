import { showFlashMessage } from "./flash_messages.js"; 

 export function fetchStockData() {
    const symbol = document.getElementById("symbolInput").value.trim().toUpperCase();
    const fetchButton = document.getElementById("fetchStockButton");
    if (!symbol) {
        showFlashMessage("Please enter a stock symbol.", "error");
        return;
    }

    fetchButton.disabled = true;
    fetchButton.innerText = "Fetching...";
    fetch("/get_stock_data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol: symbol })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showFlashMessage(data.error, "error");
            return;
        }

    
        document.getElementById("stockSymbol").innerText = data.symbol;
        document.getElementById("stockPrice").innerText = data.latest_close;
        document.getElementById("sentiment").innerText = data.average_sentiment;
        document.getElementById("recommendation").innerText = data.recommendation;

        document.getElementById("result").classList.remove("hidden");
    })
    .catch(error =>{
        console.error("Error:", error);
        showFlashMessage("An error occurred while fetching stock data.", "error");
    }).finally(()=>{
        fetchButton.disabled = false;
        fetchButton.innerText = "Fetch";
    });
}

document.getElementById("fetchStockButton").addEventListener("click", fetchStockData);