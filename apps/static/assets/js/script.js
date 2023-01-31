// Get references to the necessary DOM elements
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const conversation = document.getElementById("conversation");
const username = document.getElementById("username").textContent;
// Add an event listener to the send button to handle sending messages
sendButton.addEventListener("click", sendMessage);

// Send the user's message to the OpenAI API and display the bot's response
function sendMessage() {
  // Get the user's message from the input field
  const message = messageInput.value;
  // Display the bot's response in the conversation area
  const userMessage = document.createElement("div");
  userMessage.className = "container bg-gradient-info rounded p-2 text-white float-start"
  userMessage.innerHTML = username +": " + message;
  conversation.appendChild(userMessage);
  // Send the message to the OpenAI API
  if(window.location.pathname == '/chat'){
  fetch("/send-message", {
    method: "POST",
    body: JSON.stringify({ message }),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the bot's response in the conversation area
      const botMessage = document.createElement("div");
      botMessage.innerHTML = "Austin A.I: " + data.response;
      botMessage.className = "container bg-white rounded p-2 text-dark float-end"
      conversation.appendChild(botMessage);
    });
  }
  if(window.location.pathname == '/emoji-chat'){
    fetch("/send-message-emoji", {
      method: "POST",
      body: JSON.stringify({ message }),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
        // Display the bot's response in the conversation area
        const botMessage = document.createElement("div");
        botMessage.innerHTML = "Austin A.I: " + data.response;
        botMessage.className = "container bg-white rounded p-2 text-dark float-end"
        conversation.appendChild(botMessage);
      });
    }
  // Clear the message input field
  messageInput.value = "";
}
