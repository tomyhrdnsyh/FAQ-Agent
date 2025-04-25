from preprocessing.prompt_template import GENERATE_DESCRIPTION_PROMPT

import srsly, os
from tqdm import tqdm
from openai import OpenAI
from loguru import logger
from dotenv import load_dotenv

logger.info(f'Status load_dotenv: {load_dotenv(".env")}')


class DescriptionGenerator:
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o-mini",
        prompt_template_path: str = GENERATE_DESCRIPTION_PROMPT
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.prompt_template = prompt_template_path

    def build_prompt(self, question: str, answer: str) -> str:
        return self.prompt_template.format(question=question, answer=answer)

    def generate_description(self, question: str, answer: str) -> str:
        prompt = self.build_prompt(question, answer)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"[ERROR] Failed to generate description: {e}")
            return ""

    def process_dataset(self, input_path: str, output_path: str):
        faq_data = srsly.read_json(input_path)

        output_data = []
        for item in tqdm(faq_data, desc="Generating descriptions"):
            description = self.generate_description(item["question"], item["answer"])
            item["description"] = description
            output_data.append(item)

        srsly.write_json(output_path, output_data)


if __name__ == "__main__":
    generator = DescriptionGenerator()
    generator.process_dataset(
        input_path="data/faq.json",
        output_path="data/faq_preprocessed.json"
    )