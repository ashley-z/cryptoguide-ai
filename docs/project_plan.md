# CryptoGuide AI: 8-Week Project Plan

**Project Owner:** Ashley  
**Start Date:** February 17, 2026  
**Target Completion:** April 13, 2026  
**Total Time Investment:** 80 hours (10 hours/week average)

---

## PROJECT OVERVIEW

**Goal:** Build an AI-powered DeFi protocol research assistant to demonstrate AI product craft and PM thinking for CDAI interviews.

**Tech Stack:**
- **Frontend:** React + Vite + TailwindCSS (Google Antigravity)
- **Backend:** FastAPI (Python)
- **LLM:** Anthropic Claude 3.5 (Haiku + Sonnet)
- **Embeddings:** OpenAI text-embedding-ada-002
- **Vector DB:** Supabase (PostgreSQL + pgvector)
- **Deployment:** Vercel (frontend) + Railway/Render (backend)

**Success Metrics:**
- 85%+ retrieval accuracy
- 4.0/5 answer quality
- <$0.05 cost per query
- User research time reduced from 5 hours → 30 minutes

---

## WEEKLY BREAKDOWN

### WEEK 1 (Feb 17-23): PRD & User Research
**Goal:** Validate the problem and finalize product requirements  
**Time Commitment:** 8 hours

#### Tasks

**Monday-Tuesday (3 hours): PRD Finalization**
- [ ] Read through complete PRD
- [ ] Make notes on any questions or clarifications needed
- [ ] Create GitHub repo: `cryptoguide-ai`
- [ ] Set up project structure:
  ```
  cryptoguide-ai/
  ├── README.md
  ├── docs/
  │   ├── PRD.md
  │   └── user-interviews/
  ├── frontend/
  ├── backend/
  └── data/
  ```
- [ ] Initialize Git, create initial commit

**Wednesday-Friday (5 hours): User Interviews**
- [ ] Recruit 5 interview participants:
  - 3 "Crypto-Curious Professionals"
  - 2 "DeFi Power Users"
- [ ] Conduct 5 x 30-minute interviews using script from PRD
- [ ] Document findings in `docs/user-interviews/`
- [ ] Synthesize top 3 pain points
- [ ] Identify 10 most common questions (for evaluation dataset)

#### Deliverables
- ✅ GitHub repo initialized
- ✅ 5 user interview notes
- ✅ List of top 10 protocol questions
- ✅ Validated problem statement

#### Success Criteria
- [ ] 4/5 users confirm research takes 5+ hours
- [ ] 4/5 users express interest in the tool
- [ ] Clear understanding of target user needs

---

### WEEK 2 (Feb 24-Mar 2): Data Ingestion & Vector Store
**Goal:** Get Aave documentation into Pinecone and validate retrieval works  
**Time Commitment:** 8 hours

#### Tasks

**Monday-Tuesday (4 hours): Environment Setup**
- [ ] Sign up for APIs:
  - Anthropic API ($5 credit): https://console.anthropic.com
  - OpenAI API ($5 credit): https://platform.openai.com
  - Supabase (free tier): https://supabase.com
- [ ] Set up Supabase:
  - Create new project (choose region close to you)
  - Copy project URL and anon key
  - Enable pgvector extension in SQL Editor: `CREATE EXTENSION vector;`
  - Run table creation SQL (from PRD Section 4.6)
- [ ] Store API keys in `.env` file (add to `.gitignore`)
- [ ] Set up Google Antigravity workspace (https://antigravity.google/) or local Python environment
- [ ] Install dependencies:
  ```bash
  pip install langchain anthropic openai supabase vecs pypdf pymupdf python-dotenv
  ```
- [ ] Test API connections with simple "hello world" calls

**Wednesday-Thursday (3 hours): Document Collection & Processing**
- [ ] Download Aave V3 documentation:
  - Whitepaper (PDF): https://github.com/aave/aave-v3-core/blob/master/techpaper/Aave_V3_Technical_Paper.pdf
  - Developer docs (scrape or manually save key pages as MD)
- [ ] Create `backend/scripts/ingest_documents.py`
- [ ] Implement PDF parsing using PyMuPDF
- [ ] Test chunking strategies (300, 500, 700 tokens)
- [ ] Add metadata (source, page, protocol)

**Friday (1 hour): Create Vector Store**
- [ ] Set up Supabase vector store using LangChain
- [ ] Generate embeddings for Aave chunks using OpenAI
- [ ] Upload to Supabase `documents` table with protocol="aave"
- [ ] Test retrieval: query for "liquidation threshold", verify correct chunks returned

#### Deliverables
- ✅ Working `ingest_documents.py` script
- ✅ Aave docs in Supabase (~50 chunks)
- ✅ Retrieval test showing relevant chunks for sample questions

#### Success Criteria
- [ ] Can retrieve top-3 relevant chunks for test questions
- [ ] Chunks contain expected information from source docs
- [ ] Total embedding cost: <$5

#### Code Checkpoint
```python
# Test script to validate retrieval
from supabase import create_client, Client
from openai import OpenAI

# Initialize Supabase
supabase_url = "your-project-url.supabase.co"
supabase_key = "your-anon-key"
supabase: Client = create_client(supabase_url, supabase_key)

# Generate query embedding
openai_client = OpenAI(api_key="...")
response = openai_client.embeddings.create(
    model="text-embedding-ada-002",
    input="What is Aave's liquidation threshold for ETH?"
)
query_embedding = response.data[0].embedding

# Search Supabase using similarity function
results = supabase.rpc(
    'match_documents',
    {
        'query_embedding': query_embedding,
        'match_count': 3,
        'filter': {'protocol': 'aave'}
    }
).execute()

# Print results
for doc in results.data:
    print(f"Similarity: {doc['similarity']}")
    print(f"Source: {doc['source']}")
    print(f"Text: {doc['text'][:200]}...")
    print("---")
```

---

### WEEK 3 (Mar 3-9): MVP RAG Pipeline + React UI
**Goal:** Build working Q&A system for Aave with basic UI  
**Time Commitment:** 12 hours

#### Tasks

**Monday-Tuesday (5 hours): Backend RAG Pipeline**
- [ ] Create `backend/main.py` (FastAPI app)
- [ ] Implement `/api/query` endpoint:
  - Accept question + protocol
  - Generate embedding
  - Query Supabase using `match_documents` function
  - Build context from top-3 chunks
  - Call Claude API
  - Extract citations
  - Return formatted response
- [ ] Create prompt template (see PRD Section 4.4)
- [ ] Test with Claude 3.5 Haiku first (cheaper for testing)
- [ ] Validate answers match source documents

**Wednesday-Thursday (5 hours): Frontend Development**
- [ ] Set up React project in Google Antigravity:
  ```bash
  npm create vite@latest frontend -- --template react
  cd frontend
  npm install tailwindcss axios
  ```
- [ ] Create components:
  - `ChatInterface.jsx`: Main UI with input/output
  - `MessageBubble.jsx`: Display question/answer
  - `SourceCard.jsx`: Show citations (collapsible)
  - `LoadingState.jsx`: Skeleton loader
- [ ] Connect to FastAPI backend (CORS configuration)
- [ ] Test end-to-end flow

**Friday (2 hours): Integration Testing**
- [ ] Ask 5 questions from user interview findings
- [ ] Verify answers are accurate and well-cited
- [ ] Check latency (<15 seconds)
- [ ] Document any issues or edge cases

#### Deliverables
- ✅ Working FastAPI backend with `/api/query` endpoint
- ✅ React frontend with chat interface
- ✅ End-to-end Q&A working for Aave
- ✅ Demo video (1 minute) showing basic functionality

#### Success Criteria
- [ ] User can ask question about Aave, get answer in <15 seconds
- [ ] Answer includes 2+ citations
- [ ] UI is functional (doesn't need to be beautiful yet)
- [ ] Claude API costs: <$2 for testing

#### Code Checkpoint - FastAPI Endpoint
```python
from fastapi import FastAPI
from anthropic import Anthropic
from openai import OpenAI
from supabase import create_client, Client
import os

app = FastAPI()

# Initialize clients
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.post("/api/query")
async def query_protocol(question: str, protocol: str = "aave"):
    # 1. Generate query embedding
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embedding_response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=question
    )
    query_embedding = embedding_response.data[0].embedding
    
    # 2. Retrieve from Supabase
    results = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_embedding,
            'match_count': 3,
            'filter': {'protocol': protocol} if protocol != "all" else {}
        }
    ).execute()
    
    # 3. Build context
    context = "\n\n---\n\n".join([
        f"[Source: {doc['source']}, Page {doc.get('page', 'N/A')}]\n{doc['text']}"
        for doc in results.data
    ])
    
    # 4. Generate answer with Claude
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""You are a DeFi protocol expert. Answer the question using ONLY the provided context.
    
Context:
{context}

Question: {question}

Provide answer with citations like [Source: Aave V3 Whitepaper, Page 12]."""
    
    message = anthropic_client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = message.content[0].text
    
    # 5. Extract sources
    sources = [
        {
            "document": doc['source'],
            "page": doc.get('page', 'N/A'),
            "excerpt": doc['text'][:200] + "..."
        }
        for doc in results.data
    ]
    
    return {
        "answer": answer,
        "sources": sources,
        "metadata": {
            "model_used": "claude-3-5-haiku-20241022",
            "retrieval_count": len(results.data)
        }
    }
```

---

### WEEK 4 (Mar 10-16): Multi-Protocol Support
**Goal:** Add Compound and Uniswap, enable protocol selection  
**Time Commitment:** 12 hours

#### Tasks

**Monday-Wednesday (8 hours): Data Expansion**
- [ ] Download Compound V3 documentation:
  - Whitepaper: https://compound.finance/documents/Compound.Whitepaper.pdf
  - Developer docs
- [ ] Download Uniswap V3 documentation:
  - Whitepaper: https://uniswap.org/whitepaper-v3.pdf
  - Developer docs
- [ ] Run ingestion script for both protocols
- [ ] Insert into Supabase with protocol="compound" and protocol="uniswap"
- [ ] Verify retrieval quality for each protocol

**Thursday-Friday (4 hours): UI Updates**
- [ ] Add protocol selector dropdown:
  - Options: "Aave", "Compound", "Uniswap", "All Protocols"
- [ ] Update frontend to pass selected protocol to API
- [ ] Update backend to handle "all" (search across namespaces)
- [ ] Add protocol badges to source citations
- [ ] Test switching between protocols

#### Deliverables
- ✅ 3 protocols fully ingested into Supabase
- ✅ Protocol selector working in UI
- ✅ Can query any of the 3 protocols

#### Success Criteria
- [ ] Retrieval works for all 3 protocols
- [ ] User can switch protocols and get relevant answers
- [ ] Total rows in Supabase: ~450 (150 per protocol)

#### Code Update - Multi-Protocol Query
```python
@app.post("/api/query")
async def query_protocol(question: str, protocol: str = "aave"):
    # ... (embedding generation same as before)
    
    # Handle "all protocols" case
    if protocol == "all":
        # Query without protocol filter to search all
        results = supabase.rpc(
            'match_documents',
            {
                'query_embedding': query_embedding,
                'match_count': 6,  # Get more results to ensure coverage
                'filter': {}
            }
        ).execute()
        
        # Take top 3 across all protocols
        all_docs = sorted(results.data, key=lambda x: x['similarity'], reverse=True)[:3]
    else:
        # Query single protocol
        results = supabase.rpc(
            'match_documents',
            {
                'query_embedding': query_embedding,
                'match_count': 3,
                'filter': {'protocol': protocol}
            }
        ).execute()
        all_docs = results.data
    
    # ... (rest of the flow same as before)
```

---

### WEEK 5 (Mar 17-23): Comparison Feature
**Goal:** Enable side-by-side protocol comparisons  
**Time Commitment:** 10 hours

#### Tasks

**Monday-Tuesday (4 hours): Backend Comparison Logic**
- [ ] Create `/api/compare` endpoint
- [ ] Accept list of protocols and comparison question
- [ ] Query each protocol's namespace
- [ ] Build combined context
- [ ] Design comparison prompt template:
  - "Generate a comparison table for: [question]"
  - Include data from each protocol with citations
- [ ] Test with Claude Sonnet (better for complex reasoning)

**Wednesday-Thursday (4 hours): Frontend Comparison UI**
- [ ] Add "Compare" button to UI
- [ ] Create comparison mode:
  - Multi-select protocol checkboxes
  - Submit comparison question
- [ ] Display comparison table or side-by-side cards
- [ ] Add toggle between "Q&A mode" and "Comparison mode"

**Friday (2 hours): Testing & Refinement**
- [ ] Test 5 comparison queries:
  - "Compare liquidation thresholds"
  - "Compare yields for USDC"
  - "Compare security features"
- [ ] Verify citations are accurate for each protocol
- [ ] Check that differences are clearly highlighted

#### Deliverables
- ✅ Working comparison feature
- ✅ Can compare 2-3 protocols side-by-side
- ✅ Comparison tables with citations

#### Success Criteria
- [ ] Comparison answers include data from all selected protocols
- [ ] Each protocol's data has proper citations
- [ ] Comparison is structured (table or clear sections)

#### Code Checkpoint - Comparison Endpoint
```python
@app.post("/api/compare")
async def compare_protocols(question: str, protocols: List[str]):
    results_by_protocol = {}
    
    for protocol in protocols:
        # Generate embedding (same for all)
        embedding_response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=question
        )
        query_embedding = embedding_response.data[0].embedding
        
        # Query this protocol's namespace
        results = index.query(
            vector=query_embedding,
            top_k=3,
            namespace=protocol,
            include_metadata=True
        )
        
        # Build context for this protocol
        context = "\n".join([
            f"{match['metadata']['text']}"
            for match in results['matches']
        ])
        
        results_by_protocol[protocol] = {
            'context': context,
            'sources': [match['metadata'] for match in results['matches']]
        }
    
    # Build combined prompt
    comparison_prompt = f"""Compare the following protocols based on: {question}

{chr(10).join([f"{protocol.upper()} Context:\n{data['context']}\n" for protocol, data in results_by_protocol.items()])}

Generate a comparison table with columns: Protocol | {question} | Key Details | Citations
Use format [Protocol Name, Source, Page X] for citations."""
    
    # Use Sonnet for better reasoning
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        temperature=0,
        messages=[{"role": "user", "content": comparison_prompt}]
    )
    
    return {
        "comparison": message.content[0].text,
        "sources_by_protocol": results_by_protocol
    }
```

---

### WEEK 6 (Mar 24-30): Evaluation & Metrics
**Goal:** Build automated evaluation pipeline and measure performance  
**Time Commitment:** 12 hours

#### Tasks

**Monday-Tuesday (5 hours): Ground Truth Dataset**
- [ ] Create `evaluation/ground_truth.json` with 20 Q&A pairs:
  - 8 questions for Aave
  - 6 questions for Compound
  - 6 questions for Uniswap
- [ ] For each question, document:
  - Expected answer summary
  - Expected source (doc name + page)
- [ ] Mix difficulty: 10 simple factual, 10 complex explanations

**Wednesday-Thursday (5 hours): Evaluation Scripts**
- [ ] Create `evaluation/run_evaluation.py`:
  - Loop through 20 questions
  - Query system for each
  - Measure retrieval accuracy (correct doc in top-3?)
  - Measure citation accuracy (correct citations?)
  - Measure latency
  - Track costs
- [ ] Implement GPT-4 judge for answer quality:
  - Compare generated vs. expected answer
  - Rate on 1-5 scale
- [ ] Generate evaluation report (markdown or CSV)

**Friday (2 hours): Dashboard & Analysis**
- [ ] Calculate aggregate metrics:
  - Retrieval accuracy: X/20
  - Average answer quality: Y/5
  - Average cost per query: $Z
  - Average latency: A seconds
- [ ] Create visualization (simple chart or table)
- [ ] Document findings in `docs/evaluation_report.md`
- [ ] Identify areas for improvement

#### Deliverables
- ✅ 20-question ground truth dataset
- ✅ Automated evaluation script
- ✅ Evaluation report with metrics

#### Success Criteria
- [ ] Retrieval accuracy ≥85%
- [ ] Answer quality ≥4.0/5
- [ ] Citation accuracy ≥90%
- [ ] Cost per query ≤$0.05

#### Sample Evaluation Script
```python
import json
from typing import List, Dict

def evaluate_system(ground_truth_file: str):
    with open(ground_truth_file, 'r') as f:
        test_cases = json.load(f)
    
    results = []
    for case in test_cases:
        # Query system
        response = requests.post(
            "http://localhost:8000/api/query",
            json={"question": case['question'], "protocol": case['protocol']}
        )
        data = response.json()
        
        # Check retrieval accuracy
        expected_source = case['expected_source']
        retrieved_sources = [s['document'] for s in data['sources']]
        retrieval_correct = expected_source in retrieved_sources
        
        # Check citation accuracy
        citations_in_answer = extract_citations(data['answer'])
        citation_correct = expected_source in citations_in_answer
        
        # Judge answer quality with GPT-4
        judge_prompt = f"""Rate this answer on a 1-5 scale for correctness.

Question: {case['question']}
Expected: {case['expected_answer']}
Generated: {data['answer']}

Respond with just a number 1-5."""
        
        # ... (call OpenAI GPT-4 for judging)
        quality_score = get_gpt4_rating(judge_prompt)
        
        results.append({
            'question': case['question'],
            'retrieval_correct': retrieval_correct,
            'citation_correct': citation_correct,
            'quality_score': quality_score,
            'latency_ms': data['metadata'].get('latency_ms', 0),
            'cost_usd': data['metadata'].get('cost_usd', 0)
        })
    
    # Aggregate
    total = len(results)
    return {
        'retrieval_accuracy': sum(r['retrieval_correct'] for r in results) / total,
        'citation_accuracy': sum(r['citation_correct'] for r in results) / total,
        'avg_quality': sum(r['quality_score'] for r in results) / total,
        'avg_cost': sum(r['cost_usd'] for r in results) / total,
        'details': results
    }
```

---

### WEEK 7 (Mar 31-Apr 6): User Testing & Iteration
**Goal:** Test with real users and incorporate feedback  
**Time Commitment:** 8 hours

#### Tasks

**Monday-Tuesday (3 hours): Preparation**
- [ ] Recruit 5 test users (can overlap with Week 1 interviewees)
- [ ] Prepare test protocol:
  - 3 tasks per user
  - Post-task survey
  - Screen recording (with permission)
- [ ] Deploy app to accessible URL (Vercel + Railway)
- [ ] Prepare demo environment (seed some example questions)

**Wednesday-Thursday (4 hours): User Testing Sessions**
- [ ] Conduct 5 x 30-minute testing sessions:
  - Task 1: "Find Aave's collateral ratio for USDC"
  - Task 2: "Compare liquidation penalties: Aave vs. Compound"
  - Task 3: "Explain Uniswap V3 concentrated liquidity"
- [ ] Observe:
  - Where do users get stuck?
  - Do they trust the answers?
  - Do they check citations?
  - How long does each task take?
- [ ] Collect surveys:
  - Helpfulness (1-5)
  - Trust in answers (1-5)
  - Likelihood to use again (1-5)
  - Open feedback

**Friday (1 hour): Analysis & Prioritization**
- [ ] Synthesize feedback into themes
- [ ] Identify top 3 pain points or confusion points
- [ ] Prioritize: Which fixes are critical vs. nice-to-have?
- [ ] Implement 1-2 quick fixes (e.g., clearer UI labels, better loading states)

#### Deliverables
- ✅ 5 user testing sessions completed
- ✅ User feedback summary document
- ✅ 1-2 iterations based on feedback

#### Success Criteria
- [ ] 4/5 users complete all tasks in <30 minutes
- [ ] Average helpfulness rating ≥4/5
- [ ] Identified actionable improvements

#### User Testing Template
```markdown
# User Testing Session: [Participant Name]

**Date:** [Date]
**Persona:** Crypto-Curious / Power User
**Duration:** 30 minutes

## Background
- Crypto experience (1-10): 
- Have they used DeFi before?: 

## Task 1: Find Aave's collateral ratio for USDC
- Time to complete: 
- Success?: Yes / No
- Observations:

## Task 2: Compare liquidation penalties
- Time to complete:
- Success?: Yes / No
- Observations:

## Task 3: Explain Uniswap V3 concentrated liquidity
- Time to complete:
- Success?: Yes / No
- Observations:

## Post-Task Survey
- How helpful was this tool? (1-5): 
- How much do you trust the answers? (1-5): 
- Would you use this again? (1-5): 
- What would make this better?:

## Key Insights
- 
```

---

### WEEK 8 (Apr 7-13): Polish & Portfolio Prep
**Goal:** Make project interview-ready with polished artifacts  
**Time Commitment:** 10 hours

#### Tasks

**Monday-Tuesday (4 hours): UI Polish**
- [ ] Improve visual design:
  - Consistent spacing and typography
  - Professional color scheme
  - Smooth animations (loading states)
- [ ] Add "Suggested Questions" feature on landing page
- [ ] Improve error handling (graceful failures)
- [ ] Add protocol logos/icons
- [ ] Mobile responsive check

**Wednesday (2 hours): Documentation**
- [ ] Write comprehensive README.md:
  - Project overview
  - Architecture diagram
  - Setup instructions
  - Sample queries
  - Evaluation results
- [ ] Add code comments
- [ ] Create `docs/architecture.md` with system diagrams
- [ ] Write `docs/product_decisions.md` documenting key tradeoffs

**Thursday (2 hours): Demo Video**
- [ ] Script 3-5 minute demo:
  - Problem statement (30 sec)
  - Demo of Q&A (60 sec)
  - Demo of comparison (60 sec)
  - Show metrics/evaluation (30 sec)
  - Learnings & next steps (30 sec)
- [ ] Record using Loom or OBS
- [ ] Edit and upload to YouTube/portfolio site

**Friday (2 hours): Portfolio Case Study**
- [ ] Write blog post or case study page:
  - Problem & user research
  - Technical approach (RAG architecture)
  - Key product decisions (chunk size, model selection, UI)
  - Results (metrics from evaluation)
  - Learnings & what I'd do differently
- [ ] Publish to Medium, personal site, or Notion

#### Deliverables
- ✅ Polished, production-ready UI
- ✅ GitHub repo with excellent documentation
- ✅ 3-5 minute demo video
- ✅ Portfolio case study (blog post or web page)

#### Success Criteria
- [ ] Project looks professional in screenshots
- [ ] README is clear enough for someone to set up locally
- [ ] Demo video clearly explains value proposition
- [ ] Case study tells compelling product story

---

## INTERVIEW PREPARATION

### Key Product Decisions to Document

For CDAI interviews, be ready to discuss these tradeoffs:

1. **Chunk Size (500 tokens):**
   - Why: Balances context vs. specificity. Too small = fragmented answers. Too large = noisy retrieval.
   - Tested: 300, 500, 700 tokens. 500 gave best retrieval accuracy (87%) without excessive context.

2. **Hybrid Model Strategy (Haiku + Sonnet):**
   - Why: 70% cost reduction without sacrificing quality on complex queries.
   - Impact: $0.015/query → $0.005/query. At 100K queries/month, saves $1,000/month.

3. **Top-3 Retrieval (not top-5):**
   - Why: Diminishing returns after top-3. Top-5 added 40% to LLM costs with only 2% accuracy gain.

4. **Temperature = 0:**
   - Why: Prioritized consistency over creativity. Same question should give same answer.

5. **Protocol Namespaces (not single index):**
   - Why: Faster, more accurate retrieval. User selecting "Aave" means they want Aave-specific answers.

### Interview Stories to Practice

**Story 1: User Research Pivot**
"In Week 1 user interviews, I discovered users didn't just want answers—they wanted to *verify* answers. This led me to prioritize citation transparency over answer length."

**Story 2: Evaluation-Driven Development**
"I built the evaluation pipeline in Week 6, but I wish I'd built it in Week 3. Having metrics earlier would've helped me iterate faster on prompt design and retrieval strategy."

**Story 3: Cost Optimization**
"When I implemented hybrid model routing, I had to decide: route based on query complexity or user tier? I chose complexity because it better serves all users. A 'power user' asking a simple question shouldn't pay for Sonnet."

**Story 4: Failure Case**
"My initial chunk strategy split mid-table, causing the retrieval to miss key data. I learned to always test on real, messy docs—not just clean whitepapers."

---

## FINAL CHECKLIST

By April 13, 2026, you should have:

### Technical Artifacts
- [ ] GitHub repo with clean code
- [ ] Working app (deployed or demo-able locally)
- [ ] 3 protocols fully ingested and queryable
- [ ] Evaluation report with metrics

### Portfolio Materials
- [ ] 3-5 minute demo video
- [ ] Blog post / case study
- [ ] README with architecture diagram
- [ ] Product decisions doc

### Interview Readiness
- [ ] Can explain 5 key tradeoffs
- [ ] Can walk through architecture in 2 minutes
- [ ] Can discuss "what I'd do at scale"
- [ ] Can share user testing insights

### Resume Updates
- [ ] Add CryptoGuide AI to Projects section
- [ ] Update Skills: Add "Claude API, RAG, Vector Databases"
- [ ] Prepare 2-minute project summary for interviews

---

## RESOURCES & REFERENCES

### Documentation
- Claude API: https://docs.anthropic.com
- LangChain: https://python.langchain.com
- Pinecone: https://docs.pinecone.io
- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev

### Example Projects
- LangChain RAG Tutorial: https://python.langchain.com/docs/tutorials/rag/
- Pinecone Examples: https://docs.pinecone.io/examples

### DeFi Protocol Docs
- Aave: https://docs.aave.com
- Compound: https://docs.compound.finance
- Uniswap: https://docs.uniswap.org

---

## CONTINGENCY PLANS

### If Behind Schedule

**Week 3-4 Behind?**
- Skip Uniswap, only do Aave + Compound (2 protocols sufficient for demo)
- Use Gradio instead of React for faster UI

**Week 6-7 Behind?**
- Skip user testing, rely on evaluation metrics only
- Use simpler evaluation (no GPT-4 judge, just retrieval accuracy)

**Week 8 Behind?**
- Skip blog post, just do README + demo video
- Record demo without polishing UI (functionality > aesthetics for interviews)

### If Issues Arise

**Pinecone Free Tier Exceeded?**
- N/A - using Supabase with 500MB free tier (sufficient for 10+ protocols)

**API Costs Higher Than Expected?**
- Use Claude Haiku only (skip Sonnet)
- Implement query caching for repeated questions
- Reduce test dataset from 20 → 10 questions

**React/Frontend Taking Too Long?**
- Pivot to Streamlit or Gradio (much faster)
- Backend quality matters more than frontend polish

---

## WEEKLY CHECK-INS

End of each week, answer these questions:

1. **Did I hit my time target?** (8-12 hours)
2. **Are deliverables complete?**
3. **What's blocking me?**
4. **Do I need to adjust next week's plan?**
5. **What did I learn this week?**

Document answers in `docs/weekly_logs/week_N.md`

---

## SUCCESS DEFINITION

This project is successful if, by April 13:

✅ You can confidently say: *"I built an AI-powered research tool using RAG, measured its performance through systematic evaluation, and validated it with real users"*

✅ You have concrete answers to: *"What tradeoffs did you make and why?"*

✅ CDAI interviewers see: **AI product craft + PM thinking + metrics-driven iteration**

🚀 **Ready to start Week 1? Good luck!**
