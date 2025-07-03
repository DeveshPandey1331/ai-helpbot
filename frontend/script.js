// ✅ frontend/script.js

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const typingIndicator = document.createElement("p");
typingIndicator.className = "typing-indicator";
typingIndicator.innerText = "Bot is typing...";
chatBox.appendChild(typingIndicator);

let messageCount = 0;
const maxMessages = 100;

// Toast Notification
function showToast(message, type = 'info') {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerText = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

async function sendMessage() {
  const userMsg = userInput.value.trim();
  if (!userMsg) return;

  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  chatBox.innerHTML += `<p><strong>You:</strong> ${userMsg} <span class='timestamp'>(${timestamp})</span></p>`;
  userInput.value = "";

  typingIndicator.style.display = "block";
  chatBox.scrollTop = chatBox.scrollHeight;
  messageCount++;

  try {
    const response = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userMsg })
    });

    const data = await response.json();
    const botTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const animatedResponse = await animateBotResponse(data.answer, botTimestamp);
    chatBox.innerHTML += animatedResponse;

    if (data.sources && data.sources.length) {
      chatBox.innerHTML += `<p class='source-info'>📚 Sources: ${data.sources.join(', ')}</p>`;
    }
  } catch (error) {
    chatBox.innerHTML += `<p style='color:red;'><strong>Error:</strong> Failed to get response.</p>`;
    showToast("Failed to get response from server", "error");
  } finally {
    typingIndicator.style.display = "none";
    chatBox.scrollTop = chatBox.scrollHeight;
    if (messageCount > maxMessages) {
      chatBox.innerHTML = "<p>⚠️ Chat truncated to save memory.</p>";
      messageCount = 0;
    }
  }
}

// Animate bot response character-by-character
async function animateBotResponse(text, timestamp) {
  return new Promise(resolve => {
    let responseHTML = `<p><strong>Bot:</strong> <span id='typing-text'></span> <span class='timestamp'>(${timestamp})</span></p>`;
    chatBox.innerHTML += responseHTML;
    const typingText = document.getElementById("typing-text");
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) {
        typingText.textContent += text[i++];
        chatBox.scrollTop = chatBox.scrollHeight;
      } else {
        clearInterval(interval);
        resolve("");
      }
    }, 10);
  });
}

// Theme toggle
const toggleButton = document.createElement("button");
toggleButton.className = "toggle-theme";
toggleButton.innerText = "🌙 Toggle Theme";
document.querySelector(".navbar").appendChild(toggleButton);

let darkMode = true;
toggleButton.onclick = () => {
  darkMode = !darkMode;
  document.body.style.background = darkMode
    ? "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
    : "linear-gradient(135deg, #f0f0f0, #ffffff, #dbefff)";
  document.body.style.color = darkMode ? "#fff" : "#000";
  showToast(darkMode ? "Dark mode enabled" : "Light mode enabled", "info");
};

// Clear chat button
const clearBtn = document.createElement("button");
clearBtn.className = "toggle-theme";
clearBtn.innerText = "🗑️ Clear Chat";
document.querySelector(".navbar").appendChild(clearBtn);
clearBtn.onclick = () => {
  chatBox.innerHTML = "";
  chatBox.appendChild(typingIndicator);
  messageCount = 0;
  showToast("Chat cleared", "info");
};

// Download chat as text file
const downloadBtn = document.createElement("button");
downloadBtn.className = "toggle-theme";
downloadBtn.innerText = "📥 Save Chat";
document.querySelector(".navbar").appendChild(downloadBtn);
downloadBtn.onclick = () => {
  const blob = new Blob([chatBox.innerText], { type: 'text/plain' });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "chat_log.txt";
  a.click();
  showToast("Chat saved", "success");
};

// Auto focus input and Enter key support
userInput.focus();
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Voice-to-text input (Web Speech API)
if ('webkitSpeechRecognition' in window) {
  const micBtn = document.createElement("button");
  micBtn.className = "toggle-theme";
  micBtn.innerText = "🎤 Speak";
  document.querySelector(".navbar").appendChild(micBtn);

  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  micBtn.onclick = () => {
    recognition.start();
    showToast("Listening...", "info");
  };

  recognition.onresult = (event) => {
    userInput.value = event.results[0][0].transcript;
    showToast("Voice input received", "success");
  };

  recognition.onerror = () => {
    showToast("Voice input failed", "error");
  };
}

// Toast styles
const style = document.createElement("style");
style.innerHTML = `
  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #323232;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.9rem;
    z-index: 999;
    opacity: 0.95;
    animation: fadeInOut 3s ease-in-out;
  }
  .toast-success { background: #28a745; }
  .toast-error { background: #dc3545; }
  .toast-info { background: #007bff; }
  @keyframes fadeInOut {
    0% { opacity: 0; transform: translateX(-50%) translateY(10px); }
    10% { opacity: 1; transform: translateX(-50%) translateY(0); }
    90% { opacity: 1; }
    100% { opacity: 0; transform: translateX(-50%) translateY(10px); }
  }
`;
document.head.appendChild(style);
