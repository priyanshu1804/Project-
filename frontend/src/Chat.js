import { useState, useRef } from "react";
import axios from "axios";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [q, setQ] = useState("");
  const videoRef = useRef();

  const ask = async () => {
    if (!q) return;

    const userMsg = { type: "user", text: q };
    setMessages((prev) => [...prev, userMsg]);

    const res = await axios.get(
      `http://127.0.0.1:8000/ask?question=${q}`
    );

    const botMsg = {
      type: "bot",
      text: res.data.answer,
      timestamps: res.data.timestamps || [],
    };

    setMessages((prev) => [...prev, botMsg]);
    setQ("");
  };

  const play = (t) => {
    videoRef.current.currentTime = t;
    videoRef.current.play();
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={m.type === "user" ? "msg user" : "msg bot"}>
            <p>{m.text}</p>

            {m.timestamps &&
              m.timestamps.map((t, idx) => (
                <button key={idx} onClick={() => play(t.start)}>
                  ▶ {Math.floor(t.start)}s
                </button>
              ))}
          </div>
        ))}
      </div>

      <video ref={videoRef} controls className="video-player">
        <source src="your_video.mp4" />
      </video>

      <div className="input-box">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask anything..."
        />
        <button onClick={ask}>➤</button>
      </div>
    </div>
  );
}

export default Chat;