# Enterprise AI Platform — Architecture

## Current Architecture

```mermaid
flowchart TD

    Client[Client / API Consumer] --> API[FastAPI]

    API --> Chat[LLM / Chat Layer]
    API --> AgentService[Agent Service]

    Chat --> Prompt[Prompt Engineering]
    Prompt --> Context[Context Engineering]
    Context --> RAG[Advanced RAG]

    RAG --> Rewrite[Query Rewriting]
    RAG --> Multi[Multi-Query Retrieval]
    RAG --> Hybrid[Hybrid Search]
    RAG --> Rerank[Reranking]
    RAG --> Metadata[Metadata Filtering]

    Rewrite --> Retrieval[Vector / Semantic Search]
    Multi --> Retrieval
    Hybrid --> Retrieval
    Rerank --> Retrieval
    Metadata --> Retrieval

    AgentService --> Graph[LangGraph Workflow]

    Graph --> Agent[Agent Node]
    Agent --> Review[Review Check]

    Review -->|Automatic| Tools[Tool Node]
    Review -->|Requires approval| HITL[Human-in-the-Loop]

    Tools --> SemanticTool[Semantic Search Tool]
    Tools --> Calculator[Calculator Tool]

    SemanticTool --> Retrieval

    Graph --> Memory[Conversation Memory]