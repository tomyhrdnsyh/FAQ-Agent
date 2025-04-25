from agent.prompt_template import SYS_FINAL_INSTRUCTION
from agent.base_agent import BaseAgent

from typing import List, Dict



class FinalInstruction(BaseAgent):

    def prompt_builder(
        self, 
        query: str, 
        faq_database: List[Dict], 
        google_results: List[Dict] = []
    ) -> str:
        faq_database = self.context_builder(faq_database)
        google_results = self.context_builder(google_results, ['title', 'link', 'snippet']) if google_results else ''

        return (
            f"Question: {query}\n"
            "Below are several potential answers retrieved from the internal LinkAja FAQ database:\n"
            f"{faq_database}\n\n"
            "Additionally, here are results from Google Search (if available):\n"
            f"{google_results}"
        )
    
    def run(
        self, 
        query: str, 
        faq_database: List[Dict], 
        google_results: List[Dict] = [], 
        chat_history: List[Dict] = []
    ) -> str:
        prompt = self.prompt_builder(query, faq_database, google_results)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": SYS_FINAL_INSTRUCTION}, *chat_history, {"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()
