const chatBox = document.getElementById("ai-chat-box");
const chatMessages = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");

let conversationId = null;

function toggleChat() {
  chatBox.classList.toggle("hidden");

  if (!chatBox.classList.contains("hidden")) {
    chatInput.focus();
  }
}

async function sendMessage(event) {
  event.preventDefault();

  const userText = chatInput.value.trim();

  if (!userText) return;

  appendMessage(userText, "user");

  chatInput.value = "";
  chatInput.disabled = true;

  const loading = appendMessage("Thinking...", "ai");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message: userText,
        conversation_id: conversationId,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Request failed.");
    }

    conversationId = data.conversation_id;

    loading.remove();

    appendMessage(data.answer, "ai");
  } catch (error) {
    loading.remove();

    appendMessage("Sorry, something went wrong. Please try again.", "ai");

    console.error(error);
  } finally {
    chatInput.disabled = false;
    chatInput.focus();
  }
}

function appendMessage(text, sender) {
  const wrapper = document.createElement("div");

  wrapper.className = sender === "user" ? "chat chat-end" : "chat chat-start";

  const bubble = document.createElement("div");

  bubble.className =
    sender === "user"
      ? "chat-bubble text-sm"
      : "chat-bubble chat-bubble-primary text-sm";

  // textContent prevents HTML injection
  bubble.textContent = text;

  wrapper.appendChild(bubble);

  chatMessages.appendChild(wrapper);

  chatMessages.scrollTop = chatMessages.scrollHeight;

  return wrapper;
}

console.log("HEllo");
