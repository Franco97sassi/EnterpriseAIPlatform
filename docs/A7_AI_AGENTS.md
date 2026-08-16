# A7 - AI Agents

## Objective

Implement an agentic workflow using LangGraph with tools, state,
memory, routing and Human-in-the-Loop (HITL).

## Architecture

User Request
    |
    v
FastAPI Agent Endpoint
    |
    v
AgentService
    |
    v
LangGraph
    |
    v
Agent Node
    |
    v
Review Check
   / \
  /   \
HITL   Tool Node
        |
        v
      Result

## Components

### Agent State

The agent maintains shared workflow state including:

- messages
- user query
- rewritten query
- retrieved context
- selected tool
- tool result
- final answer
- human review flag
- metadata

### Tools

Initial tools:

- Semantic Search
- Calculator

Tools are isolated and independently testable.

### Routing

The agent analyzes the user query and selects the appropriate tool.

Current routing is deterministic and can later be extended with
LLM-based tool calling.

### Memory

Conversation history is associated with a conversation ID.

The current implementation uses in-memory storage and can later
be replaced with Redis, PostgreSQL or LangGraph checkpointing.

### LangGraph Workflow

LangGraph orchestrates the agent state and nodes.

Current workflow:

START
  -> Agent
  -> Review Check
  -> Tool or HITL
  -> END

### Human-in-the-Loop

Actions that require human approval can stop before tool execution.

The calculator workflow currently demonstrates this mechanism.

Future implementations can use persistent LangGraph checkpoints
and resumable execution.

## API

Endpoint:

POST /api/v1/agents/run

The endpoint accepts a user query, metadata, retrieved context
and an optional conversation ID.

## Testing

The implementation includes:

- state tests
- tool tests
- routing tests
- memory tests
- LangGraph workflow tests
- HITL tests
- service tests
- API integration tests

Full project regression suite:

91 tests passed.

## Design Decisions

The implementation separates:

- state
- tools
- nodes
- routing
- memory
- graph orchestration
- API layer

This keeps agent components independently testable and allows
future replacement of deterministic routing with LLM tool calling.

## Trade-offs

Memory is currently process-local and non-persistent.

Tool selection is currently deterministic rather than LLM-driven.

HITL currently demonstrates the decision boundary but does not yet
implement persistent pause/resume execution.

These capabilities can be extended during the advanced agentic and
production stages of the roadmap.