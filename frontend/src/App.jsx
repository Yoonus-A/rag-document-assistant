import { useState , useRef } from "react";
import { FileText } from "lucide-react";
import { Send } from "lucide-react";
import "./styles.css";
import Axios from "axios";
import FileUploadButton from "./FileUploadButton";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [uploadedFile, setUploadedFile] = useState(null);
  const fileInputRef = useRef(null);

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
      setUploadedFile(file);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
  };

  return (
    <div className="app">

      <header className="header">
        <div className="logo">
          Doc Assist
        </div>

        <div className="status">
          <span className={`status-label ${uploadedFile ? 'active' : 'inactive'}`}></span>
          {uploadedFile ? 'File Uploaded' : 'No File Uploaded'}
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

        {uploadedFile && (
          <div className="uploaded-file">
            <span className="file-name">{uploadedFile.name}</span>
            <button className="remove-file-button" onClick={handleRemoveFile}>Remove</button>
          </div>
        )}

        <div className="input-container">
          <FileUploadButton handleFileUpload={handleFileUpload} inputRef={fileInputRef} disabled={!!uploadedFile} />
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