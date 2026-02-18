import os
import sys
import argparse
import fitz  # PyMuPDF
from dotenv import load_dotenv
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client, Client

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """Extracts text from PDF page by page."""
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        text = " ".join(text.split())
        # Remove null bytes that cause Postgres errors
        text = text.replace('\x00', '')
        if text.strip():
            pages.append({
                "text": text,
                "page": page_num + 1,
                "source": os.path.basename(pdf_path)
            })
    print(f"  Extracted {len(pages)} pages from {pdf_path}")
    return pages

def extract_text_from_markdown(md_path: str) -> List[Dict]:
    """Extracts text from a Markdown file, splitting by headings."""
    with open(md_path, 'r') as f:
        content = f.read()
    
    # Split by ## headings to create logical sections
    sections = content.split('\n## ')
    pages = []
    for i, section in enumerate(sections):
        text = section.strip()
        if text:
            # Re-add the ## prefix for non-first sections
            if i > 0:
                text = '## ' + text
            pages.append({
                "text": text,
                "page": i + 1,
                "source": os.path.basename(md_path)
            })
    print(f"  Extracted {len(pages)} sections from {md_path}")
    return pages

def chunk_text(pages: List[Dict], protocol: str) -> List[Dict]:
    """Chunks text while preserving metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    for page in pages:
        page_chunks = text_splitter.split_text(page["text"])
        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "metadata": {
                    "source": page["source"],
                    "page": page["page"],
                    "protocol": protocol
                }
            })
    print(f"  Created {len(chunks)} chunks for '{protocol}'")
    return chunks

def ingest_to_supabase(chunks: List[Dict]):
    """Embeds and upserts chunks to Supabase."""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase credentials missing. Check .env file.")
        
    supabase: Client = create_client(supabase_url, supabase_key)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_metadatas = metadatas[i:i+batch_size]
        
        SupabaseVectorStore.from_texts(
            texts=batch_texts,
            embedding=embeddings,
            metadatas=batch_metadatas,
            client=supabase,
            table_name="documents",
            query_name="match_documents"
        )
        print(f"  Uploaded batch {i//batch_size + 1}")

def main():
    parser = argparse.ArgumentParser(description='Ingest documents into Supabase vector store')
    parser.add_argument('--protocol', required=True, help='Protocol name (aave, compound, uniswap)')
    parser.add_argument('--file', required=True, help='Path to the document file (PDF or MD)')
    args = parser.parse_args()

    protocol = args.protocol.lower()
    file_path = args.file

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"Ingesting: {os.path.basename(file_path)}")
    print(f"Protocol: {protocol}")
    print(f"{'='*50}")

    # Extract text based on file type
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        pages = extract_text_from_pdf(file_path)
    elif ext in ['.md', '.txt']:
        pages = extract_text_from_markdown(file_path)
    else:
        print(f"Error: Unsupported file type '{ext}'. Use .pdf, .md, or .txt")
        sys.exit(1)

    # Chunk
    chunks = chunk_text(pages, protocol)
    
    # Upload
    print(f"\nUploading {len(chunks)} chunks to Supabase...")
    ingest_to_supabase(chunks)
    print(f"\n✅ Ingestion complete for '{protocol}'!")

if __name__ == "__main__":
    main()
