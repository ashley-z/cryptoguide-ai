import os
from typing import List, Dict, Any
from supabase.client import create_client, Client
from langchain_openai import OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGPipeline:
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if not all([self.supabase_url, self.supabase_key, self.openai_key, self.anthropic_key]):
            raise ValueError("Missing environment variables for RAG pipeline")
            
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0,
            max_tokens=1000
        )

    def retrieve_context(self, query: str, protocol: str, k: int = 5) -> List[Dict]:
        """Retrieves relevant documents from Supabase."""
        query_vector = self.embeddings.embed_query(query)
        
        response = self.supabase.rpc(
            'match_documents',
            {
                'query_embedding': query_vector,
                'match_count': k,
                'filter': {'protocol': protocol}
            }
        ).execute()
        
        return response.data

    def format_docs(self, docs: List[Dict]) -> str:
        """Formats retrieved documents for the prompt."""
        formatted = []
        for i, doc in enumerate(docs):
            meta = doc.get('metadata', {})
            source = f"{meta.get('source', 'Unknown')} (Page {meta.get('page', '?')})"
            content = doc.get('content', '').replace('\n', ' ')
            formatted.append(f"[{i+1}] SOURCE: {source}\nCONTENT: {content}")
        return "\n\n".join(formatted)

    def generate_answer(self, query: str, protocol: str) -> Dict[str, Any]:
        """Full RAG flow: Retrieve -> Generate -> Cite."""
        
        # 1. Retrieve
        docs = self.retrieve_context(query, protocol)
        if not docs:
            return {
                "answer": "I couldn't find any specific information about that in the protocol documentation.",
                "sources": []
            }
            
        context_str = self.format_docs(docs)
        
        # 2. Prompt
        system_prompt = """You are CryptoGuide AI, an expert DeFi research assistant. 
        Answer the user's question based ONLY on the provided context. 
        
        Rules:
        - Cite your sources using square brackets like [1], [2].
        - If the answer is not in the context, say you don't know.
        - Be concise, professional, and precise.
        - Use markdown for formatting.
        
        Context:
        {context}
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{question}")
        ])
        
        # 3. Generate
        chain = prompt | self.llm | StrOutputParser()
        answer = chain.invoke({"context": context_str, "question": query})
        
        # 4. Format Output
        return {
            "answer": answer,
            "sources": [
                {
                    "id": i+1,
                    "document": doc.get('metadata', {}).get('source'),
                    "page": doc.get('metadata', {}).get('page'),
                    "text": doc.get('content')[:200] + "..."
                }
                for i, doc in enumerate(docs)
            ]
        }
