import { showFlashMessage } from "./flash_messages.js";

export function fetchStockData() {
    let symbol = document.getElementById("symbolInput").value.toUpperCase();
    if (!symbol) 
    {
        showFlashMessage("Please enter a stock symbol.", "error");
        return;
    }

    const fetchStockHistoryButton = document.getElementById("fetchStockHistoryButton");
    fetchStockHistoryButton.disabled = true;
    fetchStockHistoryButton.innerText = "Fetching...";
    fetch(`/stock_history/${symbol}`)
        .then(response => response.json())
        .then(data => {
            let tableBody = document.querySelector("#stockTable tbody");
            let stockSymbolSpan = document.getElementById("stockSymbol");
            let resultBox = document.getElementById("result");

            tableBody.innerHTML = ""; // Clear previous data
            stockSymbolSpan.textContent = symbol;
            resultBox.classList.remove("hidden");

            if (data.history && data.history.Close) {
                let dates = Object.keys(data.history.Close);
                let previousData = null;

                dates.forEach(date => {
                    let open = data.history.Open[date].toFixed(2);
                    let close = data.history.Close[date].toFixed(2);
                    let high = data.history.High[date].toFixed(2);
                    let low = data.history.Low[date].toFixed(2);
                    let volume = data.history.Volume[date].toLocaleString();

                    let changeClass = (current, previous) => {
                        if (previous === null) return "";
                        return current > previous ? " text-green-600 " : current < previous ? " text-red-600 " : "";
                    };

                    let row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${date}</td>
                        <td class="${changeClass(open, previousData?.Open)}">$${open}</td>
                        <td class="${changeClass(close, previousData?.Close)}">$${close}</td>
                        <td class="${changeClass(high, previousData?.High)}">$${high}</td>
                        <td class="${changeClass(low, previousData?.Low)}">$${low}</td>
                        <td class="${changeClass(volume, previousData?.Volume)}">${volume}</td>
                    `;

                    tableBody.appendChild(row);
                    previousData = { Open: open, Close: close, High: high, Low: low, Volume: volume }; // Update for next iteration
                });
            } else {
                tableBody.innerHTML = "<tr><td colspan='6'>No data available</td></tr>";
            }
        })
        .catch(error => {
            console.error("Error fetching stock data:", error)
            showFlashMessage("An error occurred while fetching stock data.", "error");
        }).finally(()=>{
            fetchStockHistoryButton.disabled = false;
            fetchStockHistoryButton.innerText = "Fetch";
        });
}


document.getElementById("fetchStockHistoryButton").addEventListener("click", fetchStockData);
