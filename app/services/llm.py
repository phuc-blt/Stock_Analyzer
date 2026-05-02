import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
try:
    from vllm import LLM
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False


class LLMRouter:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GOOGLE_API_KEY")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def get_openai(self):
        if not self.openai_api_key:
            raise ValueError("Missing OpenAI API key")
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=self.openai_api_key,
        )

    def get_gemini(self):
        if not self.gemini_api_key:
            raise ValueError("Missing Gemini API key")
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.2,
            google_api_key=self.gemini_api_key,
        )

    def get_vllm(self):
        if not VLLM_AVAILABLE:
            raise ValueError("vLLM not installed. Install with: pip install vllm")
        
        # Try common vLLM models
        models_to_try = [
            "qwen3.5:0.8b",  # Available local model - fastest
            "gemma4:e2b",  # Available local model
            "llama3:8b",
            "qwen:7b",
            "phi3",
            "mistral"
        ]
        
        for model in models_to_try:
            try:
                return LLM(
                    model=model,
                    temperature=0.2,
                )
            except Exception as e:
                print(f"Failed to load vLLM model {model}: {str(e)}")
                continue
        
        raise ValueError("No vLLM models available. Please install a model first.")

    def get_ollama(self):
        # Try common models, prioritize available local model
        models_to_try = [
            "qwen3.5:0.8b",  # Available local model - fastest
            "gemma4:e2b",  # Available local model
            self.ollama_model,
            "llama3:8b", 
            "qwen:7b",
            "phi3",
            "mistral"
        ]
        
        for model in models_to_try:
            try:
                return ChatOllama(
                    model=model,
                    base_url=self.ollama_base_url,
                    temperature=0.2,
                )
            except Exception as e:
                print(f"Failed to load model {model}: {str(e)}")
                continue
        
        raise ValueError("No Ollama models available. Please run 'ollama pull gemma4:e2b' to install a model.")

    def invoke(self, prompt: str):
        errors = []

        # Priority 1: OpenAI
        try:
            llm = self.get_openai()
            return llm.invoke(prompt)
        except Exception as e:
            errors.append(f"OpenAI failed: {str(e)}")

        # Priority 2: Gemini
        try:
            llm = self.get_gemini()
            return llm.invoke(prompt)
        except Exception as e:
            errors.append(f"Gemini failed: {str(e)}")

        # Priority 3: vLLM (local inference)
        try:
            llm = self.get_vllm()
            return llm.invoke(prompt)
        except Exception as e:
            errors.append(f"vLLM failed: {str(e)}")

        # Priority 4: Ollama local fallback
        try:
            llm = self.get_ollama()
            return llm.invoke(prompt)
        except Exception as e:
            errors.append(f"Ollama failed: {str(e)}")
    
        # If all LLMs fail, return error message
        return f"All LLM providers failed: {'; '.join(errors)}"


# Create global instance
llm_router = LLMRouter()