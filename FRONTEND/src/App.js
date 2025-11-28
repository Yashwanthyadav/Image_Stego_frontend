import React, { useState } from "react";

function App() {
  const [encodeImage, setEncodeImage] = useState(null);
  const [decodeImage, setDecodeImage] = useState(null);
  const [message, setMessage] = useState("");
  const [decodedText, setDecodedText] = useState("");

  const backend = "https://your-backend.onrender.com";

  const handleEncode = async () => {
    if (!encodeImage || !message) return;

    const form = new FormData();
    form.append("image", encodeImage);
    form.append("message", message);

    const res = await fetch(`${backend}/encode`, {
      method: "POST",
      body: form,
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "encoded.png";
    link.click();
  };

  const handleDecode = async () => {
    if (!decodeImage) return;

    const form = new FormData();
    form.append("image", decodeImage);

    const res = await fetch(`${backend}/decode`, {
      method: "POST",
      body: form,
    });

    const data = await res.json();
    setDecodedText(data.message);
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Image Steganography Web App</h2>

      <h3>Encode</h3>
      <input
        type="file"
        onChange={(e) => setEncodeImage(e.target.files[0])}
      />
      <input
        type="text"
        placeholder="Enter secret message"
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={handleEncode}>Encode</button>

      <h3>Decode</h3>
      <input
        type="file"
        onChange={(e) => setDecodeImage(e.target.files[0])}
      />
      <button onClick={handleDecode}>Decode</button>

      <h3>Decoded Message:</h3>
      <pre>{decodedText}</pre>
    </div>
  );
}

export default App;
