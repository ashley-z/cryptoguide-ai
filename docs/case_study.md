# CryptoGuide AI — Case Study

## The Problem

DeFi protocol research takes 5-10 hours. A typical user exploring Aave needs to read a 45-page whitepaper, browse documentation sites, search Twitter for security updates, then repeat the entire process for each protocol they want to compare. Most people give up.

**Target user:** Finance professionals exploring DeFi — they understand markets, but protocol documentation is dense and scattered.

---

## The Solution

CryptoGuide AI is a RAG-powered research assistant that answers DeFi protocol questions in ~3 seconds with cited sources. Users select a protocol, ask a question in plain English, and get an answer with expandable source citations.

### Core Features
1. **Single Protocol Q&A** — Natural language queries against Aave, Compound, or Uniswap documentation
2. **Protocol Comparison** — Side-by-side analysis with citations from both protocols
3. **Source Transparency** — Every answer includes expandable source cards showing document, page, and excerpt

---

## Architecture Decisions

### Decision 1: Claude 3 Haiku vs Sonnet

| Factor | Haiku | Sonnet |
|---|---|---|
| Cost/query | $0.0009 | $0.015 |
| Latency | ~2.5s | ~5-8s |
| Quality (eval) | 89% keyword coverage | ~95% keyword coverage |

**Choice: Haiku.** For documentation Q&A (factual retrieval, not creative reasoning), Haiku's 70% cost reduction was worth the marginal quality difference. At 10K queries/month, this saves $140/month.

### Decision 2: Supabase pgvector vs Pinecone

**Choice: Supabase.** Free tier sufficient for MVP (3 protocols × ~100 chunks = ~900KB vs 500MB limit). Using a protocol column instead of separate namespaces enabled cross-protocol queries with a single SQL `WHERE` clause.

### Decision 3: Chunk Size (500 tokens)

Tested 300, 500, and 700 token chunks. 500 tokens balanced:
- **Specificity:** Small enough to retrieve precise parameter values
- **Context:** Large enough to include surrounding explanation
- **Overlap:** 50-token overlap (10%) prevented mid-sentence cuts

### Decision 4: Static Ingestion vs Live Scraping

**Choice: Static.** Protocol documentation changes slowly (quarterly), so one-time ingestion is sufficient. This eliminates scraping complexity, rate limiting, and staleness detection from the MVP scope.

---

## Evaluation Methodology

Built an automated evaluation suite with 20 curated test cases (8 Aave, 6 Compound, 6 Uniswap) covering parameter lookups, mechanism explanations, risk analysis, and governance questions.

### Metrics Measured

| Metric | Method | Result | Target |
|---|---|---|---|
| Retrieval Accuracy | Does expected source appear in top-5? | **100%** | ≥85% |
| Keyword Coverage | % of expected terms in answer | **89%** | ≥75% |
| Citation Accuracy | Do [1], [2] references match sources? | **100%** | ≥90% |
| Latency | End-to-end pipeline timing | **3.1s** | <15s |
| Cost/Query | Token usage × model pricing | **$0.0009** | <$0.05 |

Every metric exceeded its target. Total evaluation cost: $0.018 for 20 queries.

---

## What I'd Do Differently at Scale

1. **Streaming responses** — Currently waiting for full generation before showing text. Streaming would make the 3s latency feel instant.

2. **Hybrid model routing** — Route simple factual lookups to Haiku, complex analytical questions to Sonnet. A classifier based on question complexity could optimize cost/quality tradeoffs.

3. **Response caching** — Top 20% of questions (e.g., "What is Aave?") are asked repeatedly. Caching saves ~60% of API costs.

4. **Conversation context** — Currently stateless. Adding conversation history would enable follow-ups like "Tell me more about that liquidation threshold."

5. **Real-time data integration** — Connecting to on-chain data (TVL, current rates) would bridge the gap between documentation knowledge and live protocol state.

6. **Chunk quality filtering** — Not all chunks are equally useful. Adding metadata scoring and re-ranking would improve retrieval for edge cases.

---

## Key Learnings

1. **RAG quality is dominated by chunking, not the LLM.** The difference between good and bad retrieval was in how documents were split — not which model generated the answer.

2. **Evaluation is a feature, not a chore.** Building ground truth datasets early forced clearer thinking about what "good" means and created portfolio-ready metrics.

3. **Smaller models work for constrained domains.** When the context window contains the right information, even Haiku produces excellent answers. The LLM is synthesizing, not creating.

4. **Protocol badges changed user trust.** In comparison mode, showing which source came from which protocol was the single biggest UX improvement for trust.

---

## Tech Stack

- **Frontend:** React 18 + Vite + TailwindCSS
- **Backend:** FastAPI (Python 3.11)
- **LLM:** Claude 3 Haiku (Anthropic)
- **Embeddings:** text-embedding-ada-002 (OpenAI)
- **Vector DB:** Supabase (PostgreSQL + pgvector)
- **Orchestration:** LangChain
