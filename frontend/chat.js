document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendQuery();
    }
});

async function sendQuery() {
    const userInput = document.getElementById("user-input");
    const chatArea = document.getElementById("chat-area");
    const userQuery = userInput.value.trim();

    if (!userQuery) {
        alert("Please enter a message.");
        return;
    }

    // Append user message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerHTML = `<div class="bubble">${userQuery}</div>`;
    chatArea.appendChild(userMessage);
    chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll to the latest message

    // Clear input field
    userInput.value = "";

    try {
        // Send the query to the API
        const response = await fetch("http://127.0.0.1:5000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: userQuery })
        });

        const data = await response.json();

        // Check if there was an error from the backend
        if (data.error) {
            throw new Error(data.error);
        }

        // Append bot response
        const botMessage = document.createElement("div");
        botMessage.className = "message bot";
        botMessage.innerHTML = `<div class="bubble">${data.response}</div>`;
        chatArea.appendChild(botMessage);
        chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll to the latest message
    } catch (error) {
        console.error("Error:", error);
        const errorMessage = document.createElement("div");
        errorMessage.className = "message bot";
        errorMessage.innerHTML = `<div class="bubble">Sorry, something went wrong. Please try again later.</div>`;
        chatArea.appendChild(errorMessage);
        chatArea.scrollTop = chatArea.scrollHeight;
    }
}
