# Technical Specification

## 1. System Overview

CryptoGuide AI is a Retrieval-Augmented Generation (RAG) system specialized in DeFi protocol documentation. It operates as a decoupled architecture with a React frontend, FastAPI backend, and Supabase vector store.

---

## 2. Tech Stack & Dependencies

### 2.1 Frontend
- **Framework:** React 19.2.0 (Vite 7.3.1)
- **Styling:** TailwindCSS 4.1.18 (CSS Variables + `@theme`)
- **Components:** Custom "Crystalline" design system (uncontrolled inputs, glassmorphic cards)
- **Markdown:** `react-markdown` 10.1.0

### 2.2 Backend
- **Runtime:** Python 3.11+
- **API Framework:** FastAPI 0.109+ (Uvicorn ASGI)
- **Orchestration:** LangChain (Core, OpenAI, Anthropic, Community)
- **LLM:** Anthropic Claude 3 Haiku (`claude-3-haiku-20240307`)
- **Embeddings:** OpenAI `text-embedding-ada-002`
- **Database Driver:** `supabase-py`

### 2.3 Data Layer
- **Store:** Supabase (Managed PostgreSQL 15+)
- **Vector Extension:** `pgvector`
- **Index:** IVFFlat (100 lists)
- **Dimensions:** 1536

---

## 3. API Contract

### global
- **Base URL:** `http://localhost:8000` (Dev)

### `GET /health`
Returns system status.
- **Response:** `200 OK`
```json
{
  "status": "ok",
  "pipeline_ready": true
}
```

### `POST /api/query`
Single protocol Q&A.
- **Request:**
```json
{
  "question": "What is eMode?",
  "protocol": "aave"
}
```
- **Response:**
```json
{
  "answer": "Efficiency Mode (eMode) allows...",
  "sources": [
    {
      "id": 1,
      "document": "Aave_V3_Technical_Paper.pdf",
      "page": 7,
      "text": "..."
    }
  ],
  "metadata": { "model": "claude-3-haiku-20240307" }
}
```

### `POST /api/compare`
Multi-protocol comparison.
- **Request:**
```json
{
  "question": "Compare liquidation penalties",
  "protocols": ["aave", "compound"]
}
```
- **Response:**
```json
{
  "answer": "Aave's penalty varies by asset...",
  "protocols": ["aave", "compound"],
  "sources": [...]
}
```

---

## 4. RAG Pipeline Logic

The `RAGPipeline` class (`backend/rag.py`) manages the retrieval and generation flow:

### 4.1 Initialization
- Connects to Supabase via `SUPABASE_URL` + `SUPABASE_KEY`.
- Initializes `OpenAIEmbeddings` and `ChatAnthropic` (Claude 3 Haiku, temp=0).

### 4.2 Retrieval Strategy (`retrieve_context`)
1. Embeds user query using `text-embedding-ada-002`.
2. Calls Supabase RPC `match_documents`:
   - Inputs: Query vector, match count (k=5), filter JSON.
   - Filter: `metadata->>'protocol'` match.
   - Ordering: Cosine similarity (`<=>` operator).

### 4.3 Generation Strategy (`generate_answer`)
1. Formats retrieved docs into context string: `[1] SOURCE: ... CONTENT: ...`
2. Constructs System Prompt:
   - Role: Expert DeFi assistant.
   - Constraint: Answer *only* from context.
   - Format: Use markdown, cite sources as `[1]`.
3. Invokes Chain: `Prompt | LLM | StrOutputParser`

---

## 5. Comparison Engine Logic

The `ComparisonEngine` class (`backend/compare.py`) wraps the RAG pipeline:

1. **Context Aggregation:**
   - Iterates through requested `protocols` (e.g., Aave, Compound).
   - Calls `rag.retrieve_context` for each protocol separately.
   - Combines results into a single context block, tagged by protocol.
2. **Synthesis:**
   - Uses a specialized comparison prompt: *"Compare and contrast the following protocols based on the provided context..."*
   - Forces structured side-by-side analysis.
3. **Response Assembly:**
   - Merges source lists from all retrievals.
   - Tags sources with their origin protocol for frontend badges.

---

## 6. Directory Structure

```
cryptoguide-ai/
├── backend/
│   ├── main.py          # FastAPI app & endpoints
│   ├── rag.py           # Core RAG logic
│   ├── compare.py       # Multi-protocol logic
│   ├── evaluation/      # Eval suite & datasets
│   └── scripts/         # Ingestion utilities
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.jsx      # Main layout & routing
│   │   └── index.css    # Tailwind & Design tokens
│   └── package.json     # Dependencies
└── docs/                # Project documentation
```
