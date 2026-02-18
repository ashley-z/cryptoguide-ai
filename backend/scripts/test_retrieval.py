import os
import sys
from dotenv import load_dotenv
from supabase.client import create_client, Client
from langchain_openai import OpenAIEmbeddings

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def test_retrieval(query: str, protocol: str = "aave"):
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not all([supabase_url, supabase_key, openai_key]):
        print("Error: Missing API credentials in .env file")
        return

    print(f"\n--- Testing Retrieval for: '{query}' ({protocol}) ---")
    
    # 1. Generate Embedding
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    query_vector = embeddings.embed_query(query)
    
    # 2. Query Supabase
    supabase: Client = create_client(supabase_url, supabase_key)
    
    try:
        response = supabase.rpc(
            'match_documents',
            {
                'query_embedding': query_vector,
                'match_count': 3,
                'filter': {'protocol': protocol}
            }
        ).execute()
        
        if not response.data:
            print("No results found. Did you run ingest_documents.py?")
            return

        print(f"Found {len(response.data)} relevant chunks:\n")
        
        for i, doc in enumerate(response.data):
            meta = doc.get('metadata', {})
            print(f"[{i+1}] Similarity: {doc['similarity']:.4f}")
            print(f"    Source: {meta.get('source', 'N/A')} (Page {meta.get('page', 'N/A')})")
            print(f"    Text: {doc['content'][:150]}...\n")
            
    except Exception as e:
        print(f"Error querying Supabase: {e}")
        print("Hint: Did you enable the 'vector' extension and create the 'match_documents' function in Supabase SQL Editor?")

if __name__ == "__main__":
    test_retrieval("What is the liquidation threshold?")
