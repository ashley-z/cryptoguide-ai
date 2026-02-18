-- Reset: Drop existing objects
DROP FUNCTION IF EXISTS match_documents(vector(1536), int, jsonb);
DROP TABLE IF EXISTS documents;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create documents table (simplified to match LangChain's SupabaseVectorStore defaults)
-- LangChain only writes: id, content, embedding, metadata
-- Protocol, source, page etc. are stored inside the metadata JSONB column
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content TEXT,
  embedding VECTOR(1536),
  metadata JSONB DEFAULT '{}'
);

-- Create index for fast similarity search
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create similarity search function
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding VECTOR(1536),
  match_count INT DEFAULT 3,
  filter JSONB DEFAULT '{}'
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 
    CASE 
      WHEN filter ? 'protocol' THEN 
        documents.metadata->>'protocol' = filter->>'protocol'
      ELSE TRUE
    END
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
