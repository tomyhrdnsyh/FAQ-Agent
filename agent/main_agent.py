from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv('.env')

from agent.base_agent import BaseAgent, Document
from agent.final_instruction_agent import FinalInstruction
from retriever.local_retriever import LocalRetriever
from retriever.embed_documents import EmbeddingGenerator
from retriever.web_retriever import GoogleSearcher

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class CSLinkAja(BaseAgent):
    top_k: int = 5
    hybrid_retrieve: bool = False
    
    def __post_init__(self):
        self.retriever = LocalRetriever("data/faq_embeddings.pkl")
        self.gsearch = GoogleSearcher()
        self.embedder = EmbeddingGenerator()
        self.final_instruction = FinalInstruction(model='gpt-4o')

    def local_faq_database(self, query: str) -> List[Dict]:
        query_vec = self.retriever.embed_query(self.embedder.embed_text, query)
        faq_data = self.retriever.retrieve(query_vec, top_k=self.top_k)
        return faq_data
    
    def metadata_builder(self, **kwargs):
        return {
            'id': str(uuid4()),
            **kwargs
        }

    def executor(self, query: str, chat_history: str) -> Dict:
        if self.hybrid_retrieve:
            with ThreadPoolExecutor() as executor:
                faq_data = executor.submit(self.local_faq_database, query)
                gresponse = executor.submit(self.gsearch.search, query)
                faq_data, gresponse = faq_data.result(), gresponse.result()

            final_answer = self.final_instruction.run(query, faq_data, gresponse, chat_history=chat_history)
            log_tools = [
                {'name': 'local_faq_database', 'input': query, 'output': faq_data, 'source': 'internal_faq_linkaja'},
                {'name': 'gsearch', 'input': query, 'output': gresponse, 'source': 'google'},
            ]
            metadata = self.metadata_builder(query=query, tools=log_tools)
        else:
            faq_data = self.local_faq_database(query)
            final_answer = self.final_instruction.run(query, faq_data, chat_history=chat_history)

            log_tools = [
                {'name': 'local_faq_database', 'input': query, 'output': faq_data, 'source': 'internal_faq_linkaja'}
            ]
            metadata = self.metadata_builder(query=query, tools=log_tools)

        return Document(page_content=final_answer, metadata=metadata)

    def run(self, query, chat_history: List[Dict] = []):
        document = self.executor(query, chat_history)
        return document
