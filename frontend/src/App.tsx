import { useEffect, useRef, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import "./App.css";

type IconName = "activity" | "agent" | "book" | "chat" | "check" | "chevron" | "code" | "database" | "file" | "menu" | "plus" | "search" | "send" | "spark" | "stack" | "user" | "x";
type Message = { id: string; role: "user" | "assistant"; content: string };
type AgentResult = {
  selected_tool: string | null;
  tool_result: { tool?: string; query?: string; documents?: unknown[]; count?: number; result?: unknown } | null;
  requires_human_review: boolean;
};
type ApiStatus = "checking" | "online" | "offline";

const API_URL = import.meta.env.VITE_API_URL ?? "";
const starterPrompts = [
  { icon: "search" as IconName, title: "Explore the knowledge base", text: "How does the advanced RAG pipeline work?" },
  { icon: "agent" as IconName, title: "Run an agent workflow", text: "Search our documents for the platform architecture" },
  { icon: "code" as IconName, title: "Explain the system", text: "Explain the AI platform architecture in simple terms" },
];

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, React.ReactNode> = {
    activity: <><path d="M3 12h4l2-7 4 14 2-7h6" /></>,
    agent: <><rect x="4" y="6" width="16" height="13" rx="3" /><path d="M9 10h.01M15 10h.01M9 15h6M12 2v4" /></>,
    book: <><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z" /><path d="M4 5.5v14" /></>,
    chat: <><path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z" /></>,
    check: <><path d="m5 12 4 4L19 6" /></>, chevron: <><path d="m9 18 6-6-6-6" /></>,
    code: <><path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14" /></>,
    database: <><ellipse cx="12" cy="5" rx="8" ry="3" /><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6" /></>,
    file: <><path d="M6 2h8l4 4v16H6zM14 2v5h5M9 13h6M9 17h6" /></>, menu: <><path d="M4 6h16M4 12h16M4 18h16" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>, search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
    send: <><path d="m22 2-7 20-4-9-9-4zM22 2 11 13" /></>, spark: <><path d="m12 3-1.4 4.1a5.5 5.5 0 0 1-3.5 3.5L3 12l4.1 1.4a5.5 5.5 0 0 1 3.5 3.5L12 21l1.4-4.1a5.5 5.5 0 0 1 3.5-3.5L21 12l-4.1-1.4a5.5 5.5 0 0 1-3.5-3.5z" /></>,
    stack: <><path d="m12 2 9 5-9 5-9-5zM3 12l9 5 9-5M3 17l9 5 9-5" /></>, user: <><circle cx="12" cy="8" r="4" /><path d="M4 22a8 8 0 0 1 16 0" /></>,
    x: <><path d="m6 6 12 12M18 6 6 18" /></>,
  };
  return <svg aria-hidden="true" className="icon" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [agentResult, setAgentResult] = useState<AgentResult | null>(null);
  const [status, setStatus] = useState<ApiStatus>("checking");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [conversationId] = useState(() => `demo-${crypto.randomUUID?.() ?? Date.now()}`);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${API_URL}/health`).then((response) => setStatus(response.ok ? "online" : "offline")).catch(() => setStatus("offline"));
  }, []);
  useEffect(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), [messages, loading]);

  async function sendMessage(text = input) {
    const query = text.trim();
    if (!query || loading) return;
    setMessages((current) => [...current, { id: crypto.randomUUID(), role: "user", content: query }]);
    setInput(""); setLoading(true); setAgentResult(null); setDetailsOpen(true);
    try {
      const [chatResponse, agentResponse] = await Promise.all([
        fetch(`${API_URL}/api/v1/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: query }) }),
        fetch(`${API_URL}/api/v1/agents/run`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user_query: query, conversation_id: conversationId, metadata: { channel: "interview-demo" }, retrieved_context: [] }) }).catch(() => null),
      ]);
      if (!chatResponse.ok) throw new Error(`Chat API returned ${chatResponse.status}`);
      const chatData = await chatResponse.json() as { response: string };
      if (agentResponse?.ok) setAgentResult(await agentResponse.json() as AgentResult);
      setMessages((current) => [...current, { id: crypto.randomUUID(), role: "assistant", content: chatData.response }]);
      setStatus("online");
    } catch (error) {
      setStatus("offline");
      setMessages((current) => [...current, { id: crypto.randomUUID(), role: "assistant", content: `No pude completar la solicitud. Comprueba que la API está activa en ${API_URL || "el servidor local"}.` }]);
      console.error(error);
    } finally { setLoading(false); }
  }

  function submit(event: FormEvent) { event.preventDefault(); void sendMessage(); }
  function newChat() { setMessages([]); setAgentResult(null); setInput(""); setSidebarOpen(false); }
  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); void sendMessage(); } }
  const documentCount = agentResult?.tool_result?.count ?? 0;

  return <div className="app-shell">
    {sidebarOpen && <button aria-label="Cerrar navegación" className="backdrop" onClick={() => setSidebarOpen(false)} />}
    <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
      <div className="brand"><span className="brand-mark"><Icon name="spark" size={19} /></span><div><strong>NEXUS</strong><small>Enterprise AI</small></div><button className="mobile-close" aria-label="Cerrar menú" onClick={() => setSidebarOpen(false)}><Icon name="x" /></button></div>
      <button className="new-chat" onClick={newChat}><Icon name="plus" size={16} /> New conversation</button>
      <p className="nav-label">Workspace</p>
      <nav>
        <button className="nav-item active"><Icon name="chat" /> Playground <span className="nav-pill">Live</span></button>
        <button className="nav-item"><Icon name="book" /> Knowledge base</button>
        <button className="nav-item"><Icon name="agent" /> Agent workflows</button>
        <button className="nav-item"><Icon name="activity" /> Observability</button>
      </nav>
      <p className="nav-label">Recent</p>
      <button className="recent active"><span>Advanced RAG architecture</span><small>Just now</small></button>
      <button className="recent"><span>Agent tool orchestration</span><small>Yesterday</small></button>
      <div className="sidebar-foot"><div className="avatar">AM</div><div><strong>AI Engineer</strong><small>Demo workspace</small></div><Icon name="chevron" size={16} /></div>
    </aside>

    <main className="workspace">
      <header className="topbar">
        <div className="topbar-title"><button className="menu-button" aria-label="Abrir menú" onClick={() => setSidebarOpen(true)}><Icon name="menu" /></button><div><h1>AI Playground</h1><p>Production RAG &amp; agent orchestration</p></div></div>
        <div className="topbar-actions"><span className={`api-status ${status}`}><i />{status === "checking" ? "Connecting" : status === "online" ? "All systems operational" : "API offline"}</span><span className="model-badge"><Icon name="spark" size={14} /> Gemini · Advanced RAG</span><button className="details-button" onClick={() => setDetailsOpen(!detailsOpen)}><Icon name="activity" /> Trace</button></div>
      </header>

      <section className="chat-canvas">
        {messages.length === 0 ? <div className="welcome">
          <div className="eyebrow"><span /><Icon name="spark" size={13} /> AI engineering showcase</div>
          <h2>What will we <em>build</em> today?</h2>
          <p>Query your enterprise knowledge, inspect retrieval decisions, and watch agent tools work in real time.</p>
          <div className="prompt-grid">{starterPrompts.map((prompt) => <button key={prompt.title} onClick={() => void sendMessage(prompt.text)}><span className="prompt-icon"><Icon name={prompt.icon} /></span><span><strong>{prompt.title}</strong><small>{prompt.text}</small></span><Icon name="chevron" size={16} /></button>)}</div>
          <div className="capabilities"><span><Icon name="database" size={14} /> Hybrid search</span><span><Icon name="stack" size={14} /> Reranking</span><span><Icon name="agent" size={14} /> Tool calling</span><span><Icon name="check" size={14} /> HITL ready</span></div>
        </div> : <div className="message-list">
          {messages.map((message) => <article key={message.id} className={`message ${message.role}`}><div className="message-avatar">{message.role === "user" ? <Icon name="user" size={17} /> : <Icon name="spark" size={17} />}</div><div className="message-body"><div className="message-meta"><strong>{message.role === "user" ? "You" : "Nexus Assistant"}</strong>{message.role === "assistant" && <span>Gemini</span>}</div><p>{message.content}</p>{message.role === "assistant" && <div className="answer-tags"><span><Icon name="check" size={12} /> Grounded response</span><span>{documentCount} sources</span></div>}</div></article>)}
          {loading && <article className="message assistant"><div className="message-avatar"><Icon name="spark" size={17} /></div><div className="message-body"><div className="message-meta"><strong>Nexus Assistant</strong><span>Reasoning</span></div><div className="thinking"><i /><i /><i /><span>Running retrieval and agent workflow…</span></div></div></article>}<div ref={endRef} />
        </div>}
      </section>

      <form className="composer-wrap" onSubmit={submit}><div className="composer"><textarea aria-label="Mensaje" rows={1} value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={handleKeyDown} placeholder="Ask your enterprise knowledge…" disabled={loading} /><div className="composer-row"><div><button type="button" className="tool-button"><Icon name="file" size={16} /> Attach</button><span className="rag-on"><i /> RAG enabled</span></div><button className="send-button" type="submit" disabled={!input.trim() || loading} aria-label="Enviar"><Icon name="send" size={17} /></button></div></div><p className="hint">Enter to send · Shift + Enter for a new line</p></form>
    </main>

    <aside className={`trace-panel ${detailsOpen ? "open" : ""}`}>
      <div className="trace-head"><div><span className="live-dot" /> Live execution</div><button aria-label="Cerrar panel" onClick={() => setDetailsOpen(false)}><Icon name="x" size={17} /></button></div>
      <div className="trace-summary"><p>Agent trace</p><strong>{loading ? "In progress" : agentResult ? "Completed" : "Ready"}</strong><span>{agentResult ? "Workflow executed successfully" : "Submit a prompt to inspect the run"}</span></div>
      <div className="trace-flow">
        <div className={`trace-step ${messages.length ? "done" : ""}`}><span><Icon name="chat" size={15} /></span><div><strong>Input validation</strong><small>Pydantic schema</small></div>{messages.length > 0 && <Icon name="check" size={15} />}</div>
        <div className={`trace-line ${messages.length ? "active" : ""}`} />
        <div className={`trace-step ${agentResult ? "done" : loading ? "running" : ""}`}><span><Icon name="search" size={15} /></span><div><strong>Intent routing</strong><small>{agentResult?.selected_tool ?? "Agent router"}</small></div>{agentResult && <Icon name="check" size={15} />}</div>
        <div className={`trace-line ${agentResult ? "active" : ""}`} />
        <div className={`trace-step ${agentResult ? "done" : ""}`}><span><Icon name="database" size={15} /></span><div><strong>Knowledge retrieval</strong><small>{documentCount} chunks retrieved</small></div>{agentResult && <Icon name="check" size={15} />}</div>
        <div className={`trace-line ${agentResult ? "active" : ""}`} />
        <div className={`trace-step ${agentResult ? "done" : ""}`}><span><Icon name="spark" size={15} /></span><div><strong>Response generation</strong><small>Grounded synthesis</small></div>{agentResult && <Icon name="check" size={15} />}</div>
      </div>
      <div className="trace-section"><div className="section-heading"><span>Runtime</span><small>Current request</small></div><dl><div><dt>Selected tool</dt><dd>{agentResult?.selected_tool ?? "—"}</dd></div><div><dt>Human review</dt><dd className={agentResult?.requires_human_review ? "warning" : "success"}>{agentResult?.requires_human_review ? "Required" : "Not required"}</dd></div><div><dt>Conversation</dt><dd>{conversationId.slice(-8)}</dd></div></dl></div>
      <div className="architecture-card"><span><Icon name="stack" size={17} /></span><div><strong>Production architecture</strong><small>FastAPI · LangGraph · Qdrant · Gemini</small></div></div>
    </aside>
  </div>;
}

export default App;
