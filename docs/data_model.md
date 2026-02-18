# Data Model Documentation

## Overview

CryptoGuide AI uses a hybrid data model combining structured relational data (via Supabase PostgreSQL) and unstructured vector embeddings (via pgvector). The core entity is the **Document Chunk**, which represents a semantic segment of a protocol's technical documentation.

## Schema: `documents` Table

The `documents` table stores the text chunks and their corresponding embeddings.

| Column | Type | Description |
|---|---|---|
| `id` | `UUID` | Primary Key (Default: `uuid_generate_v4()`) |
| `content` | `TEXT` | The raw text of the chunk |
| `embedding` | `VECTOR(1536)` | OpenAI `text-embedding-ada-002` vector representation |
| `metadata` | `JSONB` | Structured metadata for filtering and citation (see below) |

### SQL Definition

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content TEXT,
  embedding VECTOR(1536),
  metadata JSONB DEFAULT '{}'
);

-- Index for IVFFlat approximate nearest neighbor search
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

---

## Metadata Taxonomy (`JSONB`)

The `metadata` column allows for flexible, schema-less storage of document citations. We enforce the following schema in our ingestion pipeline:

```json
{
  "source": "string",
  "page": "integer",
  "protocol": "string"
}
```

### Fields

| Field | Type | Description | Example |
|---|---|---|---|
| `protocol` | `string` | The DeFi protocol this document belongs to. Used for filtering. | `"aave"`, `"compound"`, `"uniswap"` |
| `source` | `string` | The filename of the original document. | `"Aave_V3_Technical_Paper.pdf"` |
| `page` | `integer` | The page number (1-indexed) where the chunk corresponds. | `42` |

### Example Record

```json
{
  "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "content": "The liquidation threshold is the percentage...",
  "embedding": [0.0123, -0.0456, ...],
  "metadata": {
    "protocol": "aave",
    "source": "Aave_V3_Technical_Paper.pdf",
    "page": 12
  }
}
```

---

## Retrieval Logic

Our RAG pipeline uses `metadata` filtering to narrow the search space before (or during) vector similarity search.

**Query Pattern:**
```sql
SELECT * FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 5;
```

**Filtered Query Pattern (Single Protocol):**
```sql
SELECT * FROM documents
WHERE metadata->>'protocol' = 'aave'
ORDER BY embedding <=> query_embedding
LIMIT 5;
```

**Comparison Query Pattern:**
Since Supabase allows multiple filter conditions, comparison queries execute two separate retrievals or one broad retrieval filtered by an `OR` condition:
```sql
WHERE metadata->>'protocol' IN ('aave', 'compound')
```

---

## Ingestion Pipeline Specs

- **Chunking Strategy:** Recursive Character Split
- **Chunk Size:** 1000 characters (approx. 250-300 tokens)
- **Overlap:** 100 characters
- **Embedding Model:** `text-embedding-ada-002`
- **Vector Dimensions:** 1536
