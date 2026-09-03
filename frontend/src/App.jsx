import { useState } from "react";
import { Paperclip, Send } from "lucide-react";
import { FileText } from "lucide-react";
import "./styles.css";

function App() {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;

    console.log("Message:", message);

    setMessage("");
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    console.log("Selected file:", file);
  };

  return (
    <div className="app">

      <header className="header">
        <div className="logo">
          Doc Assist
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Ready
        </div>
      </header>


      <main className="chat-container">

        <div className="welcome">

          <div className="welcome-icon">
            <FileText size={32} />
          </div>

          <h1>
            Documents Assistant
          </h1>

          <p>
            Ask questions about the uploaded document and get answers based on the content of that document.
          </p>

        </div>

      </main>


      <div className="input-area">

        <div className="input-container">

          <label className="icon-button">
            <Paperclip size={21} />

            <input
              type="file"
              accept=".pdf,.doc,.docx,.txt"
              onChange={handleFileUpload}
            />
          </label>


          <input
            className="message-input"
            type="text"
            placeholder="Ask a question about the document..."
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleSend();
              }
            }}
          />


          <button
            className="send-button"
            onClick={handleSend}
          >
            <Send size={20} />
          </button>

        </div>

        <p className="input-hint">
          Upload a document and ask questions
        </p>

      </div>

    </div>
  );
}

export default App;