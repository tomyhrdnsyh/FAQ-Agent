from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from openai import OpenAI
from typing import Dict
import os

class Document(BaseModel):
    page_content: str
    metadata: Dict = Field(default=None)

class BaseAgent(ABC):

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None, name: str = "LinkAjaAgent") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

        self.name = name

    @abstractmethod
    def run(self, query: str, **kwargs) -> str:
        raise NotImplementedError(
            "Subclasses of BaseAgent must implement the 'run' method with the appropriate logic."
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} model={type(self.model).__name__}>"

