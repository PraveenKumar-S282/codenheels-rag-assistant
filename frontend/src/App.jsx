
import { useRef, useState } from "react";
import {
  Bot,
  MessageCircle,
  FileUp,
  Settings,
  Sparkles,
  Paperclip,
  Send,
  FileText,
  Plus,
  PanelLeftClose,
  Menu,
  UserRound,
  ArrowUpRight,
} from "lucide-react";
import "./App.css";

const suggestions = [
  {
    title: "Summarize my PDF",
    description: "Get the key points from your document",
    question: "Summarize this document",
    icon: FileText,
  },
  {
    title: "Explain a concept",
    description: "Understand difficult topics simply",
    question: "Explain the main concepts in this PDF",
    icon: Sparkles,
  },
  {
    title: "Find key information",
    description: "Search for important details",
    question: "What are the key points in this PDF?",
    icon: MessageCircle,
  },
];

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const fileInput = useRef(null);

  function handleFileChange(event) {
    const selected = event.target.files?.[0];

    if (!selected) return;

    if (!selected.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.");
      return;
    }

    setFile(selected);
    setError("");
    setMessages([]);
  }

  async function uploadPdf() {
    if (!file) {
      fileInput.current?.click();
      return;
    }

    setUploading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "PDF upload failed.");
      }

      setFile({
        ...file,
        indexed: true,
        pages: data.pages,
        chunks: data.chunks,
      });
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setUploading(false);
    }
  }

  async function sendMessage(text = question) {
    const prompt = text.trim();

    if (!prompt || sending) return;

    if (!file?.indexed) {
      setError("Upload and process a PDF before asking questions.");
      return;
    }

    setMessages((previous) => [
      ...previous,
      { role: "user", content: prompt },
    ]);
    setQuestion("");
    setSending(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: prompt }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not get an answer.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setSending(false);
    }
  }

  function startNewChat() {
    setMessages([]);
    setQuestion("");
    setError("");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Bot size={25} />
          </div>
          <div>
            <h1>Code<span>NHeels</span></h1>
            <p>Your AI knowledge assistant</p>
          </div>
        </div>

        <button className="nav-item active">
          <MessageCircle size={19} />
          <span>Chat</span>
        </button>

        <button className="nav-item" onClick={() => fileInput.current?.click()}>
          <FileUp size={19} />
          <span>Upload PDF</span>
        </button>

        <button className="nav-item" onClick={startNewChat}>
          <Plus size={19} />
          <span>New chat</span>
        </button>

        <div className="sidebar-divider" />

        <div className="document-heading">CURRENT DOCUMENT</div>

        {file?.indexed ? (
          <div className="document-card">
            <FileText size={22} className="document-icon" />
            <div className="document-info">
              <strong>{file.name}</strong>
              <span>{file.pages} pages · {file.chunks} chunks</span>
              <small>Ready to chat</small>
            </div>
          </div>
        ) : (
          <button
            className="empty-document"
            onClick={() => fileInput.current?.click()}
          >
            <FileUp size={23} />
            <span>No PDF uploaded yet</span>
            <small>Choose a document to begin</small>
          </button>
        )}

        <div className="sidebar-tip">
          <Sparkles size={20} />
          <p>Ask questions about your document and explore ideas faster.</p>
        </div>

        <div className="sidebar-footer">
          <div className="footer-logo">CodeNHeels AI</div>
          <span>Smarter questions. Better answers.</span>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <button className="mobile-menu" aria-label="Menu">
            <Menu size={21} />
          </button>
          <div className="topbar-label">
            <span className="status-dot" />
            AI DOCUMENT ASSISTANT
          </div>
          <button className="icon-button" onClick={startNewChat} title="New chat">
            <Plus size={20} />
          </button>
        </header>

        <section className="chat-workspace">
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-badge">
                <Sparkles size={17} />
                YOUR PERSONAL DOCUMENT AI
              </div>
              <div className="welcome-logo">
                <div className="welcome-logo-icon">
                  <Bot size={32} />
                </div>
                <h2>Meet Code<span>NHeels</span> AI</h2>
              </div>
              <p className="welcome-subtitle">
                Your documents hold the answers.
                <br />
                Let&apos;s discover them together.
              </p>

              <div className="feature-row">
                <div className="feature">
                  <FileUp size={20} />
                  <strong>Upload a PDF</strong>
                  <span>Bring your own document</span>
                </div>
                <div className="feature">
                  <MessageCircle size={20} />
                  <strong>Ask anything</strong>
                  <span>Explore your PDF content</span>
                </div>
                <div className="feature">
                  <FileText size={20} />
                  <strong>Find your sources</strong>
                  <span>See relevant page numbers</span>
                </div>
              </div>

              <div className="suggestion-heading">
                <Sparkles size={16} />
                GET STARTED WITH
              </div>
              <div className="suggestion-grid">
                {suggestions.map((item) => {
                  const Icon = item.icon;
                  return (
                    <button
                      className="suggestion-card"
                      key={item.title}
                      onClick={() => sendMessage(item.question)}
                    >
                      <span className="suggestion-icon">
                        <Icon size={19} />
                      </span>
                      <span className="suggestion-copy">
                        <strong>{item.title}</strong>
                        <small>{item.description}</small>
                      </span>
                      <ArrowUpRight size={16} className="suggestion-arrow" />
                    </button>
                  );
                })}
              </div>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((message, index) => (
                <article className={`message ${message.role}`} key={index}>
                  <div className="message-avatar">
                    {message.role === "assistant" ? (
                      <Bot size={19} />
                    ) : (
                      <UserRound size={19} />
                    )}
                  </div>
                  <div className="message-content">
                    <div className="message-author">
                      {message.role === "assistant" ? "CodeNHeels AI" : "You"}
                    </div>
                    <p>{message.content}</p>
                    {message.sources?.length > 0 && (
                      <div className="source-list">
                        <strong><FileText size={15} /> Sources</strong>
                        {message.sources.map((source, sourceIndex) => (
                          <div className="source-item" key={sourceIndex}>
                            <span>Page {source.page}</span>
                            <small>{source.source}</small>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </article>
              ))}
              {sending && (
                <div className="thinking">
                  <span />
                  <span />
                  <span />
                  <small>CodeNHeels is thinking...</small>
                </div>
              )}
            </div>
          )}
        </section>

        <footer className="composer-area">
          {file && !file.indexed && (
            <div className="selected-file">
              <FileText size={18} />
              <span>{file.name}</span>
              <button onClick={() => setFile(null)} aria-label="Remove file">×</button>
              <button
                className="process-button"
                onClick={uploadPdf}
                disabled={uploading}
              >
                {uploading ? "Processing..." : "Process PDF"}
              </button>
            </div>
          )}

          <div className="composer">
            <input
              ref={fileInput}
              type="file"
              accept=".pdf,application/pdf"
              hidden
              onChange={handleFileChange}
            />
            <button
              className="attach-button"
              title="Upload PDF"
              onClick={() => fileInput.current?.click()}
              disabled={uploading}
            >
              <Paperclip size={21} />
            </button>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  sendMessage();
                }
              }}
              placeholder={
                file?.indexed
                  ? "Ask anything about your PDF..."
                  : "Upload a PDF to start asking questions..."
              }
              rows={1}
            />
            <button
              className="send-button"
              onClick={() => sendMessage()}
              disabled={!question.trim() || sending}
              title="Send message"
            >
              <Send size={19} />
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}
          <p className="disclaimer">
            CodeNHeels AI answers using your uploaded PDF. Always verify important details.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;
