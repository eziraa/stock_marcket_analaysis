export function showFlashMessage(message, type) {
    let flashMessage = document.createElement("div");
    flashMessage.className = `flash-message flash-${type}`;
    flashMessage.innerHTML = `
        ${message} 
        <span class="close-btn" onclick="this.parentElement.remove();">&times;</span>
    `;

    document.getElementById("flashContainer").appendChild(flashMessage);

    // Auto-remove after 3 seconds
    setTimeout(() => flashMessage.remove(), 3000);
}
