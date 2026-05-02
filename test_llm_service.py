#!/usr/bin/env python3
"""
Test script for LLM Service with qwen3.5:0.8b model
"""

import os
import sys
import time
from app.services.llm import LLMRouter

def test_llm_service():
    """Test LLM service with different providers"""
    
    print("🧪 Testing LLM Service...")
    print("=" * 50)
    
    # Initialize LLM router
    llm_router = LLMRouter()
    
    # Test prompt
    test_prompt = "Analyze VNM (Vinamilk) stock briefly in 2 sentences."
    
    print(f"📝 Test Prompt: '{test_prompt}'")
    print("-" * 50)
    
    # Test each provider
    providers = [
        ("OpenAI", llm_router.get_openai),
        ("Gemini", llm_router.get_gemini), 
        ("vLLM", llm_router.get_vllm),
        ("Ollama", llm_router.get_ollama)
    ]
    
    for provider_name, provider_func in providers:
        print(f"\n🔍 Testing {provider_name}...")
        
        try:
            start_time = time.time()
            llm = provider_func()
            response = llm.invoke(test_prompt)
            end_time = time.time()
            
            print(f"✅ {provider_name} SUCCESS ({end_time - start_time:.2f}s)")
            print(f"📄 Response: {response[:100]}..." if len(response) > 100 else f"📄 Response: {response}")
            
        except Exception as e:
            print(f"❌ {provider_name} FAILED: {str(e)}")
    
    # Test the main invoke method (with fallback)
    print(f"\n🔄 Testing LLMRouter.invoke() with fallback...")
    try:
        start_time = time.time()
        response = llm_router.invoke(test_prompt)
        end_time = time.time()
        
        print(f"✅ LLMRouter SUCCESS ({end_time - start_time:.2f}s)")
        print(f"📄 Response: {response[:200]}..." if len(response) > 200 else f"📄 Response: {response}")
        
    except Exception as e:
        print(f"❌ LLMRouter FAILED: {str(e)}")

def test_ollama_direct():
    """Test Ollama directly with qwen3.5:0.8b"""
    print(f"\n🦙 Testing Ollama directly with qwen3.5:0.8b...")
    
    try:
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            from langchain_community.chat_models import ChatOllama
        
        ollama = ChatOllama(
            model="qwen3.5:0.8b",
            base_url="http://localhost:11434",
            temperature=0.2,
        )
        
        response = ollama.invoke("Hello, how are you?")
        print(f"✅ Direct Ollama SUCCESS")
        print(f"📄 Response: {response[:100]}..." if len(response) > 100 else f"📄 Response: {response}")
        
    except Exception as e:
        print(f"❌ Direct Ollama FAILED: {str(e)}")

def check_ollama_status():
    """Check Ollama service status"""
    print(f"\n🔍 Checking Ollama service status...")
    
    try:
        import requests
        
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama service running")
            print(f"📋 Available models:")
            for model in models:
                print(f"   - {model['name']}")
        else:
            print(f"❌ Ollama service error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ollama service not running: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting LLM Service Tests...")
    
    # Check Ollama status first
    check_ollama_status()
    
    # Test direct Ollama
    test_ollama_direct()
    
    # Test LLM service
    test_llm_service()
    
    print("\n🎉 LLM Service Tests Complete!")
