const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(
  ".chat-input form input[type='submit']"
); // Select the submit button inside the form
const chatbox = document.querySelector(".chatbox");
const chatbotCloseBtn = document.querySelector(".close-btn");
const callBtn = document.querySelector(".call-btn");
const audioCallStart = document.querySelector(".audio-call");
const endCallBtn = document.querySelector(".audio-call img");

const API_KEY = "sk-myapikey";

// websocket

// Create WebSocket connection.
const socket = new WebSocket("ws://127.0.0.1:8000/ws/sc/");

// Connection opened
socket.addEventListener("open", (event) => {
  console.log("WebSocket connection opened");
  // socket.send("Hello Server!");
});

// Listen for messages
socket.addEventListener("message", (event) => {
  // Parse the received data
  const data = JSON.parse(event.data);

  // Use the data in your frontend logic
  // For example, update the chatbox with the received message
  chatbox.appendChild(createChatLi(data.query, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);
  chatbox.appendChild(createChatLi(data.response, "incoming"));
  chatbox.scrollTo(0, chatbox.scrollHeight);
});

// Listen for close
socket.addEventListener("close", (event) => {
  console.log("WebSocket connection close: ", event);
});

const inputInitHeight = chatInput.scrollHeight;
console.log(inputInitHeight); // height - 55, in our case

// JavaScript code to send AJAX request
callBtn.addEventListener("click", function () {
  audioCallStart.classList.add("show");

  // end call on button click
  endCallBtn.addEventListener("click", () => {
    audioCallStart.classList.remove("show");
  });

  fetch("http://127.0.0.1:8000/recordAndRead/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookie
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data); // Handle the response data
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
});


// Function to get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const createChatLi = (message, className) => {
  // Create a chat <li> element with passed Message and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent =
    className === "outgoing"
      ? `<p></p>`
      : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
};

const generateResponse = (incomingChatLi) => {
  const messageElement = incomingChatLi.querySelector("p");

  // send POST request to OpenAI API with user's Message
  fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      messages: [
        {
          role: "system",
          content: userMessage,
        },
      ],
      model: "gpt-3.5-turbo",
    }),
  }).then((res) => {
    res
      .json()
      .then((data) => {
        messageElement.textContent = data.choices[0].message.content;
      })
      .catch((error) => {
        messageElement.textContent = "Error generating response";
      })
      .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight)); // auto-scrolling the chat box
  });
};

const handleChat = (e) => {
  e.preventDefault(); // prevent the default form submission behavior

  userMessage = chatInput.value.trim();
  if (!userMessage) return;

  // Append the user's userMessage to the chatbox
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight); // auto-scrolling the chat box
  chatInput.value = "";
  // Resetting the textarea height to its default height once a message is sent
  chatInput.style.height = `${inputInitHeight}px`;

  // Display "Thinking..." userMessage while waiting for the response
  setTimeout(() => {
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight); // auto-scrolling the chat box
    generateResponse(incomingChatLi);
  }, 500);
};

chatInput.addEventListener("input", () => {
  // Adjust the height of the input textarea based on its content
  chatInput.style.height = `${inputInitHeight}px`; // initial height
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat(e);
  }
});

chatbotCloseBtn.addEventListener(
  "click",
  () => (window.location.href = "http://127.0.0.1:8000/")
);

sendChatBtn.addEventListener("click", handleChat);
