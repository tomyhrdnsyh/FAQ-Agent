from agent.prompt_template import (
    SYS_IMPARTIAL_EVALUATOR, USER_IMPARTIAL_EVALUATOR
)
from agent.base_agent import BaseAgent, Document

from typing import List, Dict


class ImpartialEvaluator(BaseAgent):
    def user_prompt_builder(self, query: str, tools: List[Dict], bot_answer: str):
        ground_truth = self.context_builder(tools, fields=['question', 'answer', 'title', 'link', 'snippet', 'source'])
        return USER_IMPARTIAL_EVALUATOR.format(query=query, ground_truth=ground_truth, bot_answer=bot_answer)

    def run(self, query: str, document: Document) -> Document:
        prompt = self.user_prompt_builder(query, document.metadata['tools'], document.page_content)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": SYS_IMPARTIAL_EVALUATOR}, {"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()