import os
from typing import List, Dict, Any
from rag import RAGPipeline

class ComparisonEngine:
    def __init__(self, rag: RAGPipeline):
        self.rag = rag

    def compare_protocols(self, question: str, protocols: List[str]) -> Dict[str, Any]:
        """Compare multiple protocols on a given topic."""
        
        # 1. Retrieve context for each protocol
        all_context = {}
        all_sources = []
        source_counter = 1

        for protocol in protocols:
            docs = self.rag.retrieve_context(question, protocol, k=3)
            if docs:
                formatted = []
                for doc in docs:
                    meta = doc.get('metadata', {})
                    source = f"{meta.get('source', 'Unknown')} (Page {meta.get('page', '?')})"
                    formatted.append(f"[{source_counter}] SOURCE: {source}\nCONTENT: {doc.get('content', '')}")
                    all_sources.append({
                        "id": source_counter,
                        "protocol": protocol,
                        "document": meta.get('source'),
                        "page": meta.get('page'),
                        "text": doc.get('content', '')[:200] + "..."
                    })
                    source_counter += 1
                all_context[protocol] = "\n\n".join(formatted)
            else:
                all_context[protocol] = "No documentation found for this protocol."

        # 2. Build comparison prompt
        context_sections = []
        for protocol, context in all_context.items():
            context_sections.append(f"=== {protocol.upper()} ===\n{context}")
        
        combined_context = "\n\n".join(context_sections)
        
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        system_prompt = """You are CryptoGuide AI, an expert DeFi research assistant.
        Compare the following protocols based on the user's question.
        
        Rules:
        - Structure your response with clear sections for each protocol.
        - Highlight key differences and similarities.
        - Cite sources using square brackets like [1], [2].
        - Use markdown formatting with headers and bullet points.
        - If information is missing for a protocol, state that clearly.
        
        Context:
        {context}
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{question}")
        ])
        
        # 3. Generate comparison
        chain = prompt | self.rag.llm | StrOutputParser()
        answer = chain.invoke({"context": combined_context, "question": question})
        
        return {
            "answer": answer,
            "protocols": protocols,
            "sources": all_sources
        }
