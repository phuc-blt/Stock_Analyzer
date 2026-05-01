from pathlib import Path


class BaseAgent:
    def __init__(self, prompt_file: str, llm=None):
        self.prompt = Path(prompt_file).read_text(encoding="utf-8")
        self.llm = llm

    def run_llm(self, variables: dict):
        if not self.llm:
            return ""

        prompt = self.prompt.format(**variables)
        response = self.llm.invoke(prompt)
        
        # Handle different response types
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)