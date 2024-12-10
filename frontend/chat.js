async function sendQuery() {
    const userQuery = document.getElementById("user-input").value;
    const chatArea = document.getElementById("chat-area");

    if (!userQuery.trim()) {
        alert("Please enter a query.");
        return;
    }

    // Append user's message to chat
    chatArea.innerHTML += `<div class="user-message">${userQuery}</div>`;

    // Send query to API
    const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery }),
    });

    const data = await response.json();

    // Append chatbot's response to chat
    if (data.response) {
        chatArea.innerHTML += `<div class="bot-message">${data.response}</div>`;
    } else {
        chatArea.innerHTML += `<div class="bot-message">Something went wrong. Please try again.</div>`;
    }

    // Clear input field
    document.getElementById("user-input").value = "";
}
