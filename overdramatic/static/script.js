async function sendReflection() {
  const text = document.getElementById("userInput").value.trim();
  if (!text) return;

  const chatBox = document.getElementById("chatBox");
  chatBox.innerHTML += `<div><strong>You:</strong> ${text}</div>`;

  const res = await fetch("/reflect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  if (!res.ok) {
    chatBox.innerHTML += `<div><strong>Coach:</strong> Server error. Try again later.</div>`;
    return;
  }

  const data = await res.json();
  chatBox.innerHTML += `<div><strong>Coach:</strong> ${data.response.replace(/\n/g, "<br>")}</div>`;
  document.getElementById("userInput").value = "";
  chatBox.scrollTop = chatBox.scrollHeight;
}
