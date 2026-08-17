 import { useState } from "react";
import "./App.css";

type Message = {
  id: number;
  role: "user" | "assistant";
  content: string;
};

type AgentResult = {
  selected_tool: string | null;
  tool_result: {
    tool?: string;
    query?: string;
    documents?: unknown[];
    count?: number;
  } | null;
  requires_human_review: boolean;
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [agentResult, setAgentResult] = useState<AgentResult | null>(null);

  const sendMessage = async () => {
    const text = input.trim();

    if (!text || loading) return;

    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setAgentResult(null);

    try {
      // 1. Chat normal
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Chat HTTP error: ${response.status}`);
      }

      const data = await response.json();

      // 2. Ejecución del agente
      const agentResponse = await fetch(
        "http://127.0.0.1:8000/api/v1/agents/run",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_query: text,
            conversation_id: "demo-001",
            metadata: {},
            retrieved_context: [],
          }),
        }
      );

      if (!agentResponse.ok) {
        throw new Error(`Agent HTTP error: ${agentResponse.status}`);
      }

      const agentData = await agentResponse.json();

console.log("AGENT DATA:", agentData);

setAgentResult(agentData);
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      const errorMessage: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content:
          "I couldn't connect to the AI backend. Please verify that the API is running.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  const newChat = () => {
    setMessages([]);
    setInput("");
    setAgentResult(null);
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div>
          <h2>Enterprise AI</h2>
          <p className="subtitle">AI Platform</p>
        </div>

        <button className="new-chat" onClick={newChat}>
          + New Chat
        </button>

        <nav>
          <button className="nav-item active">
            💬 Chat
          </button>

          <button className="nav-item">
            📄 Documents
          </button>

          <button className="nav-item">
            🤖 Agents
          </button>

          <button className="nav-item">
            ⚙️ Settings
          </button>
        </nav>
      </aside>

      <main className="chat-section">
        <header className="topbar">
          <div>
            <h1>AI Assistant</h1>
            <span>RAG + Agentic AI</span>
          </div>

          <div className="status">
            <span className="status-dot" />
            Online
          </div>
        </header>

        <section className="messages">
          {messages.length === 0 ? (
            <div className="welcome">
              <h2>Enterprise AI Assistant</h2>

              <p>
                Ask questions, retrieve knowledge and execute
                intelligent agent workflows.
              </p>
            </div>
          ) : (
            <div className="message-list">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message-row ${message.role}`}
                >
                  <div
                    className={`message-bubble ${message.role}`}
                  >
                    <div className="message-role">
                      {message.role === "user"
                        ? "You"
                        : "AI Assistant"}
                    </div>

                    {message.content}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="message-bubble assistant">
                    <div className="message-role">
                      AI Assistant
                    </div>

                    Thinking...
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        <div className="input-area">
          <input
            value={input}
            placeholder="Ask something..."
            onChange={(event) =>
              setInput(event.target.value)
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </main>

      <aside className="activity-panel">
        <h3>Agent Activity</h3>

        <div className="activity-item">
          <span>✓</span>

          {loading
            ? "Processing request..."
            : agentResult?.selected_tool
              ? `Tool: ${agentResult.selected_tool}`
              : "Waiting for task"}
        </div>

        <h3 className="section-title">
          Sources
        </h3>

        {agentResult?.tool_result ? (
          <div className="agent-details">
            <p>
              <strong>Query:</strong>{" "}
              {agentResult.tool_result.query ?? "—"}
            </p>

            <p>
              <strong>Documents:</strong>{" "}
              {agentResult.tool_result.count ?? 0}
            </p>
          </div>
        ) : (
          <p className="empty-text">
            No sources yet
          </p>
        )}

        <h3 className="section-title">
          Human Approval
        </h3>

        <p className="empty-text">
          {agentResult?.requires_human_review
            ? "Human review required"
            : "No pending actions"}
        </p>
      </aside>
    </div>
  );
}

export default App;