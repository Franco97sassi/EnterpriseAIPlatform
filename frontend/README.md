# Nexus interview demo

The React + TypeScript frontend is an interview-ready control plane for the Enterprise AI Platform. It exposes the chat experience and, at the same time, makes the engineering behind a response visible through the live agent trace.

## Run locally

Start the API from the repository root:

```bash
uvicorn app.main:app --reload
```

Then start the UI:

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` and `/health` to `http://127.0.0.1:8000`, so local development does not depend on hardcoded browser URLs. For a deployed API, set `VITE_API_URL` at build time.

## Architecture decisions

- **One interview narrative:** starter prompts highlight advanced RAG, agent orchestration, and platform architecture instead of presenting unrelated feature pages.
- **Observable by design:** the trace panel shows validation, routing, retrieval, generation, selected tools, source counts, and HITL state alongside each answer.
- **Independent API calls:** chat and agent execution run concurrently. A successful chat remains useful if optional trace data is unavailable.
- **No UI dependency overhead:** the interface uses a small local SVG icon system and responsive CSS without adding component-library dependencies.
- **Responsive demo:** navigation and trace panels become drawers on smaller screens, retaining the complete desktop workflow on a laptop, tablet, or phone.

## Verification

```bash
npm run lint
npm run build
```
