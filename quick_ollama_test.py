#!/usr/bin/env python3
"""
Quick Ollama Performance Test
"""

import time
import sys
import os

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_ollama_basic():
    """Test basic Ollama connection and response time"""
    print("🔍 Testing Ollama basic performance...")
    
    try:
        from app.services.llm import llm_router
        
        # Test 1: Connection
        print("1. Testing connection...")
        start = time.time()
        llm = llm_router.get_ollama()
        conn_time = time.time() - start
        print(f"   ✅ Connection: {conn_time:.2f}s")
        
        # Test 2: Simple response
        print("2. Testing simple response...")
        start = time.time()
        response = llm_router.invoke("Say hello")
        resp_time = time.time() - start
        print(f"   ✅ Response: {resp_time:.2f}s")
        print(f"   📝 Response: {response}")
        
        # Test 3: Stock analysis style
        print("3. Testing stock analysis style...")
        prompt = "Analyze VNM stock briefly. Give BUY/SELL/HOLD recommendation."
        start = time.time()
        response = llm_router.invoke(prompt)
        analysis_time = time.time() - start
        print(f"   ✅ Analysis: {analysis_time:.2f}s")
        print(f"   📝 Length: {len(str(response))} chars")
        
        # Analysis
        print("\n📊 PERFORMANCE ANALYSIS:")
        print(f"   Connection: {conn_time:.2f}s")
        print(f"   Simple: {resp_time:.2f}s")
        print(f"   Analysis: {analysis_time:.2f}s")
        
        if analysis_time > 30:
            print("   ⚠️  Analysis is very slow!")
            print("   💡 Recommendations:")
            print("      - Use smaller model (phi3, qwen:7b)")
            print("      - Reduce prompt complexity")
            print("      - Check system resources")
        elif analysis_time > 10:
            print("   ⚠️  Analysis is slow but acceptable")
        else:
            print("   ✅ Performance is good")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_multi_agent_estimate():
    """Estimate multi-agent total time"""
    print("\n🤖 Multi-Agent Time Estimate:")
    
    # Based on single analysis time
    try:
        from app.services.llm import llm_router
        
        # Test single agent response
        prompt = "Analyze technical indicators for VNM stock. Keep under 100 words."
        start = time.time()
        response = llm_router.invoke(prompt)
        single_time = time.time() - start
        
        # Multi-agent has 6 agents
        agents = ["Planner", "Market", "Technical", "News", "Risk", "Decision"]
        estimated_total = single_time * len(agents)
        
        print(f"   Single agent: {single_time:.2f}s")
        print(f"   6 agents total: {estimated_total:.2f}s")
        
        if estimated_total > 120:
            print("   ⚠️  Multi-agent will be very slow (>2 minutes)")
        elif estimated_total > 60:
            print("   ⚠️  Multi-agent will be slow (>1 minute)")
        else:
            print("   ✅ Multi-agent should be acceptable")
            
        return estimated_total
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return 0

def main():
    print("🚀 Quick Ollama Performance Test")
    print("=" * 40)
    
    # Test basic performance
    if test_ollama_basic():
        # Estimate multi-agent time
        test_multi_agent_estimate()
        
        print("\n💡 OPTIMIZATION SUGGESTIONS:")
        print("1. If analysis > 30s:")
        print("   - Pull smaller model: ollama pull phi3")
        print("   - Use qwen:7b instead of gemma4")
        print("2. If multi-agent > 60s:")
        print("   - Consider concurrent processing")
        print("   - Cache repeated responses")
        print("   - Use shorter prompts")
        print("3. System optimization:")
        print("   - Close other applications")
        print("   - Check RAM usage")
        print("   - Restart Ollama service")
    else:
        print("\n❌ Ollama not working - check:")
        print("   - Ollama service: ollama serve")
        print("   - Model availability: ollama list")
        print("   - Network connection")

if __name__ == "__main__":
    main()
