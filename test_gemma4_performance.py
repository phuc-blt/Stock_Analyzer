#!/usr/bin/env python3
"""
Test Gemma4 Performance and Optimization Suggestions
"""

import time
import sys
import os

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_gemma4_performance():
    """Test gemma4:e2b performance"""
    print("🔍 Testing Gemma4:e2b Performance...")
    
    try:
        from app.services.llm import llm_router
        
        # Test 1: Simple response
        print("1. Testing simple response...")
        start = time.time()
        response = llm_router.invoke("Say hello")
        simple_time = time.time() - start
        print(f"   ✅ Simple: {simple_time:.2f}s")
        
        # Test 2: Stock analysis
        print("2. Testing stock analysis...")
        prompt = "Analyze VNM stock briefly. Give BUY/SELL/HOLD recommendation."
        start = time.time()
        response = llm_router.invoke(prompt)
        analysis_time = time.time() - start
        print(f"   ✅ Analysis: {analysis_time:.2f}s")
        print(f"   📝 Length: {len(str(response))} chars")
        
        # Test 3: Multi-agent estimate
        print("3. Multi-agent estimate...")
        estimated_total = analysis_time * 6  # 6 agents
        print(f"   📊 Estimated total: {estimated_total:.2f}s")
        
        # Analysis
        print("\n📊 PERFORMANCE ANALYSIS:")
        print(f"   Simple response: {simple_time:.2f}s")
        print(f"   Stock analysis: {analysis_time:.2f}s")
        print(f"   Multi-agent total: {estimated_total:.2f}s")
        
        if analysis_time > 30:
            print("   ⚠️  Gemma4 is slow for analysis")
            print("   💡 OPTIMIZATION SUGGESTIONS:")
            print("      1. Pull smaller model:")
            print("         ollama pull phi3")
            print("         ollama pull qwen:7b")
            print("      2. Reduce prompt complexity")
            print("      3. Use shorter prompts")
            print("      4. Consider concurrent processing")
        elif analysis_time > 15:
            print("   ⚠️  Gemma4 is moderate speed")
            print("   💡 Some optimizations may help")
        else:
            print("   ✅ Gemma4 performance is acceptable")
            
        return analysis_time, estimated_total
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return 0, 0

def suggest_optimizations(analysis_time, estimated_total):
    """Suggest optimizations based on performance"""
    print("\n🚀 OPTIMIZATION RECOMMENDATIONS:")
    
    if analysis_time > 30:
        print("🔴 IMMEDIATE ACTIONS NEEDED:")
        print("1. Install smaller model:")
        print("   ollama pull phi3  (2.2GB, fastest)")
        print("   ollama pull qwen:7b  (4.1GB, good balance)")
        print("\n2. Update LLM service priority:")
        print("   - Move phi3/qwen to top of model list")
        print("   - Keep gemma4 as fallback")
        
    if estimated_total > 120:
        print("🔴 MULTI-AGENT TOO SLOW:")
        print("1. Implement concurrent processing")
        print("2. Add response caching")
        print("3. Use shorter, focused prompts")
        
    print("\n💡 SYSTEM OPTIMIZATIONS:")
    print("• Close other applications")
    print("• Check RAM usage (need 8GB+ for Gemma4)")
    print("• Restart Ollama service: ollama serve")
    print("• Consider GPU acceleration if available")

def main():
    print("🚀 Gemma4 Performance Test")
    print("=" * 40)
    
    analysis_time, estimated_total = test_gemma4_performance()
    
    if analysis_time > 0:
        suggest_optimizations(analysis_time, estimated_total)
        
        print("\n📋 NEXT STEPS:")
        if analysis_time > 20:
            print("1. Pull smaller model: ollama pull phi3")
            print("2. Test again with new model")
            print("3. Update model priority in LLM service")
        else:
            print("1. Current performance is acceptable")
            print("2. Monitor for further optimization")
    else:
        print("\n❌ Cannot test - check Ollama service")

if __name__ == "__main__":
    main()
