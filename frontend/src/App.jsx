import { useState } from "react";
import { Paperclip, Send } from "lucide-react";
import { FileText } from "lucide-react";
import "./styles.css";
import Axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const handleSend = async () => {
    if (!message.trim()) return;

    setChatHistory((prevHistory) => [
      ...prevHistory,
      { role: "user", text: message },
    ]);
    const currentMessage = message;

    try {
      const response = await Axios.post("http://localhost:8000/process_question", {
        question: currentMessage,
      });
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { role: "assistant", text: response.data.message },
      ]);
    }
    catch (error) {
      console.error("Error sending message:", error);
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { role: "assistant", text: "Error processing your question." },
      ]);
    }

    

    setMessage("");
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await Axios.post("http://localhost:8000/file_upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("File uploaded successfully:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }


    
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
        {chatHistory.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">
              <FileText size={32} />
            </div>
            <h1>Documents Assistant</h1>
            <p>Ask questions about the uploaded document and get answers based on the content of that document.</p>
          </div>
        ) : (
          <div className="chat-window">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`chat-bubble ${msg.role}`}>
                {msg.text}
              </div>
            ))}
          </div>
        )}
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