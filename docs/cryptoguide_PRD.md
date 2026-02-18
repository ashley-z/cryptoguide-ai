# PRODUCT REQUIREMENTS DOCUMENT: CryptoGuide AI

**Project Owner:** Ashley  
**Created:** February 17, 2026  
**Target Launch:** April 13, 2026 (8 weeks)  
**Status:** Phase 0 - Product Definition

---

## EXECUTIVE SUMMARY

**What:** An AI-powered research assistant that helps non-technical users understand and compare DeFi protocols through natural language Q&A over protocol documentation.

**Why:** DeFi protocol research currently requires 5-10 hours of reading scattered documentation (whitepapers, docs sites, Discord). This creates a barrier to entry for traditional finance professionals transitioning into crypto.

**How:** RAG (Retrieval-Augmented Generation) architecture using Claude 3.5, Pinecone vector search, and semantic embeddings to provide accurate, cited answers in <30 seconds.

**Success:** Reduce protocol research time by 90% (5 hours → 30 minutes) while maintaining 85%+ citation accuracy.

---

## 1. PROBLEM STATEMENT

### Current User Journey (AS-IS)

**Persona:** Sarah, 28, former fintech analyst exploring DeFi  
**Goal:** Understand if Aave is safe for lending USDC

**Current Process:**
1. Google "Aave protocol risks" → 20+ tabs open
2. Read Aave whitepaper (45 pages, 2 hours)
3. Browse docs site for liquidation parameters (30 min)
4. Search Twitter for recent security issues (1 hour)
5. Compare to Compound by repeating steps 1-4 (2 hours)
6. Still uncertain about specific parameters (collateral ratios, liquidation thresholds)

**Total Time:** 5-10 hours  
**Outcome:** Overwhelmed, confused, often gives up

### Desired User Journey (TO-BE)

1. Ask: *"What are the risks of supplying USDC to Aave V3?"*
2. Receive answer in 15 seconds with citations to whitepaper, docs, audits
3. Follow-up: *"How does this compare to Compound?"*
4. Get side-by-side comparison table
5. Click citations to deep-dive into specific sections

**Total Time:** 30 minutes  
**Outcome:** Confident understanding with verifiable sources

---

## 2. USER RESEARCH & VALIDATION

### Target Personas

**Primary: "Crypto-Curious Professional"**
- Age: 25-35
- Background: Traditional finance, tech, biotech (like Ashley)
- Crypto Experience: Owns some BTC/ETH, wants to explore DeFi
- Pain Point: Technical docs overwhelming, no clear starting point
- Success Metric: Can explain protocol risks to a friend after 30 min

**Secondary: "DeFi Power User"**
- Age: 22-40
- Background: Crypto-native, developer, or trader
- Crypto Experience: Active DeFi user across 5+ protocols
- Pain Point: Wastes time searching for specific parameters across docs
- Success Metric: Finds specific parameter (e.g., liquidation threshold) in <1 min

### Validation Plan (Week 1)

**User Interviews (5 people):**
1. Recruit 3 "Crypto-Curious" + 2 "Power Users" from personal network
2. Ask: *"Walk me through the last time you tried to learn about a DeFi protocol"*
3. Identify: Where did they get stuck? What questions went unanswered?
4. Validate: Would an AI assistant solve this? What features matter most?

**Success Criteria:**
- 4/5 users confirm research takes 5+ hours
- 4/5 users express interest in trying the tool
- Identify top 3 most common questions (used for testing dataset)

---

## 3. GOALS & SUCCESS METRICS

### Product Goals

**Primary Goal:** Demonstrate AI product craft and PM thinking for CDAI interviews

**Secondary Goals:**
1. Ship a working RAG application using modern AI stack
2. Measure and optimize system performance (retrieval accuracy, answer quality)
3. Create portfolio artifact showcasing product decisions and tradeoffs

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **User Efficiency** | 90% reduction in research time (5hr → 30min) | User testing with 5 participants, timed tasks |
| **Retrieval Accuracy** | 85%+ of queries retrieve correct context | Automated evaluation on 20-question test set |
| **Answer Quality** | 4.0/5.0 average rating | GPT-4 as judge scoring correctness + citations |
| **Citation Accuracy** | 90%+ of answers cite correct sources | Manual review + automated source validation |
| **Cost Efficiency** | <$0.05 per query | Track API costs per question answered |
| **User Satisfaction** | 4/5+ rating on helpfulness | Post-session survey with test users |

### Anti-Goals (Out of Scope for MVP)

- Real-time on-chain data (prices, TVL)
- Financial advice or recommendations
- User authentication or saved chat history
- Mobile app
- Support for >5 protocols

---

## 4. TECHNICAL ARCHITECTURE

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│         React App (Google Antigravity + Vite + Tailwind)        │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Query      │  │  Retrieval   │  │  LLM Generation      │  │
│  │  Processing  │─▶│   Engine     │─▶│  (Claude 3.5)        │  │
│  └──────────────┘  └──────┬───────┘  └──────────────────────┘  │
│                            │                                      │
│                            ▼                                      │
│                  ┌──────────────────┐                           │
│                  │  Vector Search   │                           │
│                  │ (Supabase+pgvec) │                           │
│                  └──────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │   DOCUMENT PROCESSING         │
              │  (One-time ingestion)         │
              │  1. PDF/MD parsing            │
              │  2. Chunking (500 tokens)     │
              │  3. Embedding generation      │
              │  4. Vector storage in Postgres│
              └──────────────────────────────┘
```

### Component Specifications

#### 4.1 Frontend (React + Google IDX)

**Tech Stack:**
- **Framework:** React 18 + Vite
- **Styling:** TailwindCSS
- **UI Components:** shadcn/ui (optional, for professional look)
- **State Management:** React Context or Zustand (for chat history)
- **HTTP Client:** Axios or Fetch API
- **IDE:** Google Antigravity (https://antigravity.google/ - AI-powered development environment)

**Key Components:**
```
src/
├── components/
│   ├── ChatInterface.jsx       # Main chat UI
│   ├── MessageBubble.jsx        # Individual message display
│   ├── SourceCard.jsx           # Citation display with expandable details
│   ├── ProtocolSelector.jsx    # Dropdown for protocol selection
│   ├── LoadingState.jsx         # Skeleton loader while waiting for response
│   └── SuggestedQuestions.jsx  # Pre-populated question examples
├── services/
│   └── api.js                   # API calls to FastAPI backend
├── hooks/
│   └── useChat.js               # Custom hook for chat state management
└── App.jsx
```

**User Flow:**
1. User lands on page → sees protocol selector + suggested questions
2. User types question → clicks "Ask"
3. Loading state (skeleton UI) → API call to backend
4. Response renders with answer + expandable source citations
5. User can follow-up with another question (context maintained)

---

#### 4.2 Backend API (FastAPI)

**Tech Stack:**
- **Framework:** FastAPI (Python 3.11+)
- **LLM Integration:** LangChain + Anthropic SDK
- **Vector DB Client:** Supabase Python SDK
- **Embeddings:** OpenAI `text-embedding-ada-002`

**API Endpoints:**

**POST /api/query**
```json
Request:
{
  "question": "What are the risks of supplying USDC to Aave?",
  "protocol": "aave",
  "conversation_id": "uuid"
}

Response:
{
  "answer": "Supplying USDC to Aave V3 carries several risks...",
  "sources": [
    {
      "document": "Aave V3 Whitepaper",
      "page": 12,
      "excerpt": "Liquidation occurs when...",
      "url": "https://docs.aave.com/..."
    }
  ],
  "metadata": {
    "retrieval_time_ms": 234,
    "generation_time_ms": 1842,
    "cost_usd": 0.0023,
    "model_used": "claude-3-5-sonnet-20241022"
  }
}
```

**POST /api/compare**
```json
Request:
{
  "question": "Compare liquidation thresholds",
  "protocols": ["aave", "compound", "maker"]
}

Response:
{
  "comparison": {
    "aave": { "answer": "...", "sources": [...] },
    "compound": { "answer": "...", "sources": [...] },
    "maker": { "answer": "...", "sources": [...] }
  },
  "summary_table": "| Protocol | Threshold | ... |"
}
```

**GET /api/protocols**
```json
Response:
{
  "protocols": [
    { "id": "aave", "name": "Aave", "doc_count": 47 },
    { "id": "compound", "name": "Compound", "doc_count": 31 }
  ]
}
```

---

#### 4.3 Document Processing Pipeline

**Ingestion Flow:**
```python
# One-time setup script: ingest_documents.py

1. Load documents (PDF, Markdown)
   ├── Aave V3 Whitepaper (PDF)
   ├── Aave V3 Technical Docs (scraped HTML → MD)
   └── Aave V3 Security Audit (PDF)

2. Parse & Clean
   ├── Extract text using PyMuPDF (for PDFs)
   ├── Clean formatting (remove headers/footers)
   └── Preserve structure (headers, lists, tables)

3. Chunk Strategy
   ├── Chunk size: 500 tokens (~375 words)
   ├── Overlap: 50 tokens (10% overlap)
   ├── Preserve semantic boundaries (don't split mid-sentence)
   └── Add metadata: {source, page, section_title}

4. Generate Embeddings
   ├── Model: text-embedding-ada-002 (OpenAI)
   ├── Dimension: 1536
   └── Cost: ~$0.10 per 1M tokens

5. Store in Supabase (PostgreSQL + pgvector)
   ├── Table name: "documents"
   ├── Protocol column for filtering: "aave", "compound", etc.
   └── Metadata: {text, source, page, protocol, doc_type}
```

**Chunking Example:**
```
Original text (from Aave whitepaper, page 12):
"The Liquidation Threshold is the percentage at which a position is 
defined as undercollateralized. For example, a Liquidation Threshold 
of 80% means that if the value of the collateral falls below 80% of 
the borrowed amount, the position can be liquidated. Each asset has 
a specific liquidation threshold based on its risk profile."

Chunk 1 (with metadata):
{
  "text": "The Liquidation Threshold is the percentage at which...",
  "metadata": {
    "source": "aave-v3-whitepaper.pdf",
    "page": 12,
    "section": "Risk Parameters",
    "protocol": "aave"
  }
}
```

---

#### 4.4 RAG Pipeline

**Step-by-Step Flow:**

**Step 1: Query Processing**
```python
def process_query(question: str, protocol: str = "all"):
    # 1. Generate query embedding
    query_embedding = get_embedding(question)
    
    # 2. Determine search scope (protocol filter)
    protocol_filter = None if protocol == "all" else protocol
    
    # 3. Retrieve relevant chunks using Supabase similarity search
    results = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_embedding,
            'match_count': 3,  # Retrieve top 3 most relevant chunks
            'filter': {'protocol': protocol_filter} if protocol_filter else {}
        }
    ).execute()
    
    return results.data
```

**Step 2: Context Assembly**
```python
def build_context(results):
    context_parts = []
    for doc in results:
        context_parts.append(
            f"[Source: {doc['source']}, Page {doc['page']}]\n"
            f"{doc['text']}\n"
        )
    return "\n---\n".join(context_parts)
```

**Step 3: LLM Generation (Claude 3.5)**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT_TEMPLATE = """You are a DeFi protocol expert helping users understand cryptocurrency protocols.

CRITICAL RULES:
1. Answer ONLY using the provided context below
2. If the context doesn't contain the answer, say "I don't have enough information in the documentation to answer that"
3. ALWAYS cite which document and page number you're using
4. Be concise but thorough (2-3 paragraphs max)
5. Use plain language - explain technical terms

CONTEXT:
{context}

USER QUESTION:
{question}

Provide your answer with inline citations like [Source: Aave V3 Whitepaper, Page 12].
"""

def generate_answer(question: str, context: str, model: str = "claude-3-5-sonnet-20241022"):
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,  # Deterministic for consistency
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text
```

**Step 4: Source Extraction**
```python
def extract_sources(answer: str, retrieved_docs):
    """Parse citations from answer and match to source documents"""
    sources = []
    for doc in retrieved_docs:
        # Check if this doc was cited in the answer
        source_name = doc['source']
        if source_name in answer:
            sources.append({
                'document': source_name,
                'page': doc['page'],
                'excerpt': doc['text'][:200] + "...",
                'url': doc.get('url', '')
            })
    return sources
```

---

#### 4.5 Cost Optimization Strategy (Hybrid Model Approach)

**Tiered Model Selection:**

```python
def select_model(question: str, protocol: str):
    """
    Route queries to appropriate Claude model based on complexity
    
    Simple queries (factual lookups) → Claude 3.5 Haiku ($0.25/$1.25 per 1M tokens)
    Complex queries (comparisons, analysis) → Claude 3.5 Sonnet ($3/$15 per 1M tokens)
    """
    
    # Complexity heuristics
    complexity_signals = {
        'comparison_keywords': ['compare', 'difference', 'versus', 'vs', 'better'],
        'multi_protocol': protocol == "all" or "," in protocol,
        'analysis_keywords': ['analyze', 'explain why', 'how does', 'what if'],
        'long_question': len(question.split()) > 20
    }
    
    complexity_score = sum([
        any(kw in question.lower() for kw in complexity_signals['comparison_keywords']),
        complexity_signals['multi_protocol'],
        any(kw in question.lower() for kw in complexity_signals['analysis_keywords']),
        complexity_signals['long_question']
    ])
    
    if complexity_score >= 2:
        return "claude-3-5-sonnet-20241022"  # High quality for complex queries
    else:
        return "claude-3-5-haiku-20241022"   # Fast & cheap for simple queries

# Example usage:
model = select_model("What is Aave's liquidation threshold for ETH?", "aave")
# Returns: "claude-3-5-haiku-20241022"

model = select_model("Compare liquidation mechanisms across Aave, Compound, and Maker", "all")
# Returns: "claude-3-5-sonnet-20241022"
```

**Cost Analysis:**

| Query Type | Model Used | Avg Tokens | Cost per Query | % of Traffic |
|------------|------------|------------|----------------|--------------|
| Simple lookup | Haiku | 800 in + 200 out | $0.0005 | 60% |
| Detailed explanation | Sonnet | 1200 in + 400 out | $0.0096 | 30% |
| Multi-protocol comparison | Sonnet | 2000 in + 600 out | $0.0150 | 10% |

**Weighted Average Cost:** (0.60 × $0.0005) + (0.30 × $0.0096) + (0.10 × $0.015) = **$0.0048 per query**

**Cost Savings vs. Sonnet-only:** 70% reduction ($0.015 → $0.0048)

**At Scale:**
- 10K queries/month = $48/month (vs. $150 with Sonnet-only)
- 100K queries/month = $480/month (vs. $1,500)

---

#### 4.6 Vector Database (Supabase + pgvector)

**PostgreSQL Setup:**

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  protocol TEXT NOT NULL,
  source TEXT NOT NULL,
  page INTEGER,
  section TEXT,
  doc_type TEXT,
  text TEXT NOT NULL,
  embedding VECTOR(1536),  -- OpenAI embedding dimension
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for fast similarity search
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index for protocol filtering
CREATE INDEX idx_documents_protocol ON documents(protocol);

-- Create similarity search function
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding VECTOR(1536),
  match_count INT DEFAULT 3,
  filter JSONB DEFAULT '{}'
)
RETURNS TABLE (
  id BIGINT,
  protocol TEXT,
  source TEXT,
  page INTEGER,
  text TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.protocol,
    documents.source,
    documents.page,
    documents.text,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 
    CASE 
      WHEN filter ? 'protocol' THEN 
        documents.protocol = (filter->>'protocol')
      ELSE TRUE
    END
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

**Python Integration:**

```python
from supabase import create_client, Client
from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings import OpenAIEmbeddings

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Create vector store with LangChain
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents"
)

# Insert documents (one-time ingestion)
vector_store.add_texts(
    texts=chunk_texts,
    metadatas=[{
        "protocol": "aave",
        "source": "aave-v3-whitepaper.pdf",
        "page": 12,
        "doc_type": "whitepaper"
    }]
)

# Query documents
results = vector_store.similarity_search_with_score(
    query="What is the liquidation threshold?",
    k=3,
    filter={"protocol": "aave"}
)
```

**Protocol Organization Strategy:**
```
Table: documents
├── protocol = "aave" (150 rows)
├── protocol = "compound" (150 rows)
└── protocol = "uniswap" (150 rows)
Total: ~450 rows
```

**Why Protocol Column (not namespaces):** 
- Allows protocol-specific searches using WHERE clause
- Enables multi-protocol comparisons (query without filter)
- Standard SQL indexing for fast filtering
- Can add more metadata columns easily (date_added, version, etc.)

**Supabase Free Tier Limits:**
- 500 MB database storage
- 2 GB bandwidth per month
- Unlimited API requests
- **Sufficient for MVP** (3 protocols × 150 chunks × ~2KB per chunk = ~900KB, well under 500MB)

---

## 5. FEATURE REQUIREMENTS

### MVP Features (Phase 1-2, Weeks 1-5)

#### F1: Basic Q&A (Week 2-3)
**User Story:** As a user, I want to ask questions about a single DeFi protocol and get accurate answers with citations.

**Acceptance Criteria:**
- [ ] User can select protocol from dropdown (Aave only in Week 2)
- [ ] User can type question in text input
- [ ] System returns answer in <15 seconds
- [ ] Answer includes 2-3 inline citations
- [ ] Citations show document name + page number
- [ ] System handles "I don't know" gracefully when context insufficient

**Technical Implementation:**
- Protocol selector → filters Pinecone namespace
- Question → embedding → top-3 retrieval → Claude Haiku/Sonnet → formatted response

---

#### F2: Source Transparency (Week 3)
**User Story:** As a user, I want to see excerpts from source documents so I can verify the AI's answer.

**Acceptance Criteria:**
- [ ] Each citation is clickable/expandable
- [ ] Expanding shows 200-character excerpt from source
- [ ] Source card shows: document name, page, excerpt, link (if available)
- [ ] User can collapse/expand all sources at once

**Design Mockup:**
```
┌─────────────────────────────────────────┐
│ Answer:                                  │
│ Aave's liquidation threshold for ETH     │
│ is 82.5% [1]. This means...              │
│                                          │
│ Sources:                                 │
│ ▼ [1] Aave V3 Whitepaper, Page 12       │
│   "The liquidation threshold represents  │
│    the maximum LTV ratio... ETH: 82.5%"  │
│   📄 View full document                  │
│                                          │
│ ▶ [2] Aave V3 Docs: Risk Parameters      │
└─────────────────────────────────────────┘
```

---

#### F3: Multi-Protocol Support (Week 4-5)
**User Story:** As a user, I want to ask questions about multiple protocols (Aave, Compound, Uniswap).

**Acceptance Criteria:**
- [ ] Protocol selector includes: Aave, Compound, Uniswap, "All Protocols"
- [ ] Selecting "All Protocols" searches across all namespaces
- [ ] System correctly routes query to appropriate namespace(s)
- [ ] Answer differentiates between protocols if multiple mentioned

**Example Query:**
*User selects "All Protocols", asks: "Which protocol has the highest yield for USDC?"*

System searches all namespaces, retrieves relevant context from each, generates comparative answer.

---

#### F4: Protocol Comparison (Week 5)
**User Story:** As a user, I want to compare specific features across protocols side-by-side.

**Acceptance Criteria:**
- [ ] User can trigger comparison mode (e.g., "Compare liquidation across Aave and Compound")
- [ ] System generates structured comparison (table or side-by-side cards)
- [ ] Each protocol's data includes citations
- [ ] Comparison highlights key differences

**Example Output:**
```
| Feature           | Aave              | Compound          |
|-------------------|-------------------|-------------------|
| Liquidation       | 82.5% LTV [1]     | 75% LTV [2]       |
| Threshold (ETH)   |                   |                   |
| Liquidation       | 5% bonus [1]      | 8% incentive [2]  |
| Penalty           |                   |                   |
```

---

### Post-MVP Features (Phase 4+, Optional)

#### F5: Suggested Questions
- Display 3-5 example questions on landing page
- Categorized: "Getting Started", "Advanced", "Comparisons"
- One-click to populate input field

#### F6: Chat History
- Store last 5 Q&A pairs in session
- Allow users to reference previous questions
- Clear history button

#### F7: Cost Dashboard (Internal)
- Track costs per query, per day, per protocol
- Display in admin panel
- Identify cost outliers (unusually expensive queries)

---

## 6. EVALUATION & TESTING STRATEGY

### 6.1 Automated Evaluation (Week 6)

**Ground Truth Dataset (20 Questions):**

| Protocol | Question | Expected Answer Source |
|----------|----------|------------------------|
| Aave | What is the liquidation threshold for ETH? | Aave V3 Whitepaper, Page 12: 82.5% |
| Aave | What happens during liquidation? | Aave V3 Docs, Risk Parameters section |
| Compound | What is cUSDC? | Compound Whitepaper, Page 3 |
| Uniswap | How does concentrated liquidity work? | Uniswap V3 Whitepaper, Page 5 |
| ... | ... | ... |

**Metrics to Track:**

1. **Retrieval Accuracy:** Did the correct document chunk appear in top-3 results?
   - Tool: Compare retrieved chunks against ground truth
   - Target: 85%+

2. **Answer Correctness:** Is the answer factually accurate?
   - Tool: GPT-4 as judge (compare generated answer to ground truth)
   - Prompt: *"Rate this answer on correctness (1-5 scale)"*
   - Target: 4.0/5 average

3. **Citation Accuracy:** Does the answer cite the correct sources?
   - Tool: Regex to extract citations, match against retrieved docs
   - Target: 90%+

4. **Latency:** How long does a query take?
   - Target: <15 seconds end-to-end (retrieval + generation)

5. **Cost per Query:** How much does each query cost?
   - Target: <$0.05 (embedding + retrieval + LLM)

**Automated Evaluation Script:**
```python
def evaluate_system(test_dataset):
    results = []
    for test_case in test_dataset:
        # Run query
        response = query_system(test_case['question'], test_case['protocol'])
        
        # Measure retrieval accuracy
        retrieval_correct = check_retrieval(response['sources'], test_case['expected_source'])
        
        # Measure answer quality (GPT-4 judge)
        quality_score = judge_answer(response['answer'], test_case['expected_answer'])
        
        # Measure citation accuracy
        citation_correct = validate_citations(response['answer'], response['sources'])
        
        results.append({
            'question': test_case['question'],
            'retrieval_accurate': retrieval_correct,
            'answer_quality': quality_score,
            'citations_valid': citation_correct,
            'latency_ms': response['metadata']['retrieval_time_ms'] + response['metadata']['generation_time_ms'],
            'cost_usd': response['metadata']['cost_usd']
        })
    
    return aggregate_results(results)
```

---

### 6.2 User Testing (Week 7)

**Test Protocol:**
1. Recruit 5 users (3 "Crypto-Curious" + 2 "Power Users")
2. Give 3 tasks:
   - **Task 1:** "Find out what collateral ratio Aave requires for USDC"
   - **Task 2:** "Compare liquidation penalties between Aave and Compound"
   - **Task 3:** "Explain how Uniswap V3 concentrated liquidity works in simple terms"
3. Observe: How long does each task take? Do they trust the answers? Do they click sources?
4. Survey: Rate helpfulness (1-5), likelihood to use again (1-5), what would you change?

**Success Criteria:**
- 4/5 users complete all tasks in <30 minutes
- 4/5 users rate helpfulness 4+ out of 5
- Collect 10+ qualitative insights for iteration

---

## 7. COST ANALYSIS

### Development Costs (One-Time)

| Item | Cost |
|------|------|
| OpenAI embeddings (3 protocols, ~150 docs, 50K tokens) | $5 |
| Claude API (testing, ~500 queries during dev) | $5-10 |
| Supabase (Free tier) | $0 |
| Google Antigravity (Free tier) | $0 |
| **TOTAL** | **$10-15** |

### Operational Costs (Per Month)

**Assumptions:**
- 1,000 queries/month (generous for demo/portfolio project)
- 70% simple queries (Haiku), 30% complex (Sonnet)

| Cost Component | Calculation | Monthly Cost |
|----------------|-------------|--------------|
| Claude Haiku (700 queries) | 700 × $0.0005 | $0.35 |
| Claude Sonnet (300 queries) | 300 × $0.012 | $3.60 |
| Supabase (Free tier) | 500MB storage, 2GB bandwidth | $0 |
| **TOTAL** | | **~$4/month** |

**At Scale (10K queries/month):** ~$40/month  
**At Scale (100K queries/month):** ~$400/month

**Cost Optimization Opportunities:**
1. Cache frequent questions (e.g., "What is Aave?")
2. Use smaller embeddings model (reduce Pinecone storage)
3. Implement rate limiting for free tier users
4. Batch process queries during off-peak hours

---

## 8. RISKS & MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Claude API rate limits hit during demo** | Medium | High | Pre-generate answers for demo questions, cache results |
| **Poor retrieval quality (chunks don't contain answer)** | Medium | High | Iterate on chunk size (test 300, 500, 700 tokens), add overlap |
| **LLM hallucinates despite context** | Low | High | Use temperature=0, add "only use context" instruction, test thoroughly |
| **Supabase free tier storage exceeded** | Low | Medium | Free tier has 500MB (enough for 10+ protocols at current chunk size) |
| **Google Antigravity downtime/issues** | Low | Low | Backup: VSCode locally, deploy to Vercel |
| **Scope creep (too many features)** | High | Medium | Ruthlessly prioritize MVP, defer F5-F7 to post-MVP |

---

## 9. SUCCESS CRITERIA & DEMO READINESS

### By April 13, 2026, the project is "demo-ready" if:

✅ **Product Functionality:**
- [ ] User can ask questions about 3 protocols (Aave, Compound, Uniswap)
- [ ] System returns accurate answers with citations in <15 seconds
- [ ] Comparison feature works for 2+ protocols
- [ ] UI is polished and professional (no broken layouts, clear UX)

✅ **Technical Validation:**
- [ ] Retrieval accuracy ≥85% on 20-question test set
- [ ] Answer quality ≥4.0/5 (GPT-4 judge)
- [ ] Citation accuracy ≥90%
- [ ] Cost per query <$0.05

✅ **Portfolio Artifacts:**
- [ ] GitHub repo with clean README + architecture diagram
- [ ] 3-5 minute demo video showing key features
- [ ] Blog post / case study documenting product decisions
- [ ] Evaluation report with metrics dashboard

✅ **Interview Readiness:**
- [ ] Can explain 5 key product decisions and tradeoffs
- [ ] Can walk through technical architecture in 2 minutes
- [ ] Can discuss learnings and "what I'd do differently at scale"

---

## 10. OPEN QUESTIONS & DECISIONS NEEDED

### Week 1 Decisions:

1. **Document Selection:** Which 3 protocols should we start with?
   - **Recommendation:** Aave (lending), Uniswap (DEX), Compound (lending) → covers 2 different protocol types
   - **Alternative:** Aave, Compound, Maker → all lending, easier comparison

2. **Data Sources:** Which documents to ingest per protocol?
   - **Minimum:** Whitepaper + official docs site
   - **Nice-to-have:** Security audits, GitHub README
   - **Decision:** Start with whitepaper only (Week 2), add docs site (Week 3)

3. **Chunk Size:** 500 tokens vs. 700 tokens vs. 300 tokens?
   - **Hypothesis:** 500 tokens balances context and specificity
   - **Decision:** Test all three in Week 2, choose based on retrieval accuracy

4. **UI Framework:** Use shadcn/ui components or build custom?
   - **Tradeoff:** shadcn = faster but learning curve; custom = more control
   - **Decision:** Use shadcn/ui for speed (pre-built chat components)

5. **Deployment:** Deploy to live URL or keep local?
   - **Recommendation:** Deploy to Vercel for portfolio (shareable link)
   - **Alternative:** Keep local, record demo video

---

## 11. TIMELINE & MILESTONES

| Week | Phase | Key Deliverable | Hours |
|------|-------|-----------------|-------|
| **1** (Feb 17-23) | **PRD & User Research** | Completed PRD, 5 user interviews | 8 |
| **2** (Feb 24-Mar 2) | **Data Ingestion** | Aave docs in Pinecone, basic retrieval working | 8 |
| **3** (Mar 3-9) | **MVP RAG Pipeline** | Working Q&A for Aave, React UI prototype | 12 |
| **4** (Mar 10-16) | **Multi-Protocol** | Add Compound + Uniswap, protocol selector | 12 |
| **5** (Mar 17-23) | **Comparison Feature** | Side-by-side protocol comparison working | 10 |
| **6** (Mar 24-30) | **Evaluation** | Automated test suite, metrics dashboard | 12 |
| **7** (Mar 31-Apr 6) | **User Testing** | 5 user tests, iteration based on feedback | 8 |
| **8** (Apr 7-13) | **Polish & Portfolio** | Demo video, blog post, GitHub README | 10 |
| **TOTAL** | **8 weeks** | **Interview-ready AI product** | **80 hours** |

---

## APPENDIX A: Example User Interview Script

**Introduction (2 min):**
*"Hi [Name], thanks for chatting with me! I'm exploring a product idea for helping people research DeFi protocols more efficiently. This is just a conversation—I'm not selling anything or asking you to sign up. I want to understand your current experience with learning about crypto protocols."*

**Background Questions (5 min):**
1. How familiar are you with DeFi? (1-10 scale)
2. Have you ever tried to research a DeFi protocol before using it? Which one(s)?
3. Walk me through the last time you tried to learn about a protocol. Where did you go? What did you do?

**Pain Point Discovery (10 min):**
4. What was the hardest part of that process?
5. How long did it take you to feel confident you understood the protocol?
6. What information was easy to find? What was hard to find?
7. Did you ever give up on researching a protocol? Why?

**Solution Validation (8 min):**
8. *[Show concept sketch: AI assistant that answers protocol questions with citations]*
   What's your first reaction to this?
9. What questions would you want to ask it?
10. Would you trust the answers? What would make you trust them more?
11. How much would you be willing to pay for this? (Free, $5/month, $10/month, $20/month)

**Wrap-Up (2 min):**
12. Anything else you'd want this tool to do?
13. Would you be willing to test an early version?

---

## APPENDIX B: Resume Bullet Options

**Option 1 (Technical Depth):**
*"Architected and deployed AI-powered DeFi research assistant using RAG (Retrieval-Augmented Generation) with Claude 3.5, Pinecone vector database, and React; reduced protocol research time by 90% (5 hours → 30 minutes) through semantic search over 150+ pages of documentation across 3 protocols (Aave, Compound, Uniswap)"*

**Option 2 (Product + Metrics):**
*"Built LLM-powered protocol comparison tool achieving 87% retrieval accuracy and 4.2/5 answer quality through evaluation-driven development; implemented hybrid model routing (Claude Haiku/Sonnet) reducing cost-per-query by 70% ($0.015 → $0.005), demonstrating cost optimization at scale; validated product-market fit through user testing with 5 target personas"*

**Option 3 (PM Thinking):**
*"Led end-to-end product development of AI research assistant, conducting user interviews to validate problem (5-10 hour research burden), defining success metrics (85%+ retrieval accuracy), and documenting 10+ product tradeoffs (chunk size, model selection, UI complexity); created evaluation pipeline enabling data-driven iteration on prompt engineering and architecture decisions"*

**Recommendation for CDAI:** Option 2 or 3 (emphasizes metrics + PM process)

---

## NEXT STEPS

**Immediate Actions (This Week):**
1. ✅ Review and approve this PRD
2. [ ] Set up Google Antigravity workspace (https://antigravity.google/) with React + Vite starter
3. [ ] Create GitHub repo with initial structure
4. [ ] Sign up for APIs:
   - Anthropic (Claude) - $5 credit to start
   - OpenAI (embeddings) - $5 credit
   - Supabase (free tier) - https://supabase.com
5. [ ] Schedule 5 user interviews for Week 1
6. [ ] Download Aave V3 whitepaper + docs

**Week 1 Goal:** Complete user interviews + have PRD finalized

---

**Questions or changes before we proceed to Week 1 execution?** 🚀
