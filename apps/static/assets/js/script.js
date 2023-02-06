// Get references to the necessary DOM elements
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const conversation = document.getElementById("conversation");
const username = document.getElementById("username").textContent;
// Add an event listener to the send button to handle sending messages
sendButton.addEventListener("click", sendMessage);
document.addEventListener("keydown", function(event) { if (event.keyCode == 13) { sendButton.click(); } });
// Send the user's message to the OpenAI API and display the bot's response
function sendMessage() {
  // Get the user's message from the input field
  const message = messageInput.value;
  // Display the bot's response in the conversation area
  const userMessage = document.createElement("div");
  userMessage.className = "chat-box left-chat-box bg-gradient-info rounded p-2 text-white"
  userMessage.innerHTML = username +": " + message;
  conversation.appendChild(userMessage);
  // Send the message to the OpenAI API
  if(window.location.pathname == '/chat'){
    let dots = 0;
    function addDot() {
      let dot = ".";
      dots++;
      if (dots > 3) {
        dots = 0;
      }
      for (let i = 0; i < dots; i++) {
        dot += ".";
      }
      console.log(dot);
    }
    setInterval(addDot, 500);
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
      botMessage.className = "chat-box right-chat-box bg-white rounded p-2 text-dark"
      conversation.appendChild(botMessage);
    });
  }
  if(window.location.pathname == '/emoji-chat'){
    let dots = 0;
    const botMessage = document.createElement("div");
    conversation.appendChild(botMessage);
    
    function addDot() {
      let dot = ".";
      dots++;
      if (dots > 3) {
        dots = 0;
      }
      for (let i = 0; i < dots; i++) {
        dot += ".";
      }
      botMessage.innerHTML = "Austin A.I" + dot;
      botMessage.className = "chat-box right-chat-box bg-white rounded p-2 text-dark"
    }
    
    let intervalId = setInterval(addDot, 500);
    
    fetch("/send-message-emoji", {
      method: "POST",
      body: JSON.stringify({ message }),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
      clearInterval(intervalId);
      botMessage.innerHTML = "";
        // Display the bot's response in the conversation area
        botMessage.innerHTML = "Austin A.I: " + data.response;
        botMessage.className = "chat-box right-chat-box bg-white rounded p-2 text-dark"
        conversation.appendChild(botMessage);
      });
    }
  // Clear the message input field
  messageInput.value = "";
}
