from pathlib import Path
from loguru import logger
from typing import Callable, List

import hashlib, srsly, serpapi, os


class SearchCache:
    def __init__(self, cache_path: Path = Path("web/search_cache.json")):
        self.cache_path = cache_path
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache = self._load_cache()

    def _load_cache(self) -> dict:
        if self.cache_path.exists():
            return srsly.read_json(self.cache_path)
        return {}

    def _save_cache(self):
        srsly.write_json(self.cache_path, self.cache)

    def _hash_query(self, query: str) -> str:
        return hashlib.md5(query.strip().lower().encode()).hexdigest()

    def query(self, query: str, perform_search_fn: Callable[[str], List[str]]) -> List[str]:
        q_hash = self._hash_query(query)

        if q_hash in self.cache:
            logger.info("[Cache Hit] Returning cached results.")
            return self.cache[q_hash]

        logger.info("[Cache Miss] Performing web search...")
        result = perform_search_fn(query)
        self.cache[q_hash] = result
        self._save_cache()
        return result


class GoogleSearcher:
    def __init__(self, api_key: str = None, cache: SearchCache = None):
        self.api_key = api_key or os.environ.get("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SerpAPI API key is required. Set it via env `SERPAPI_API_KEY`.")
        self.client = serpapi.Client(api_key=self.api_key)
        self.cache = cache or SearchCache()

    def search(self, query: str) -> List[str]:
        logger.info(f"Searching Google for: {query}")
        
        def _perform_search(q: str) -> List[str]:
            results = self.client.search({
                'engine': 'google',
                'q': q,
                'num': 5
            })
            return [
                { 
                    key: value for key, value in result.items() if key in ['title', 'link', 'snippet']
                }
                for result in results.get("organic_results", [])
                if result.get("title") and result.get("link")
            ]
        
        return self.cache.query(query, _perform_search)