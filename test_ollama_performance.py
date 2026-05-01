#!/usr/bin/env python3
"""
Vietnam Stock Analyzer - Ollama Performance Test
"""

import time
import sys
import os
from datetime import datetime

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.services.llm import llm_router
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the Stock_Analyzer directory")
    sys.exit(1)

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🔍 Testing Ollama connection...")
    
    try:
        start_time = time.time()
        llm = llm_router.get_ollama()
        connection_time = time.time() - start_time
        
        print(f"✅ Ollama connection successful: {connection_time:.2f}s")
        return True, connection_time
    except Exception as e:
        print(f"❌ Ollama connection failed: {str(e)}")
        return False, 0

def test_simple_prompt():
    """Test simple prompt response time"""
    print("\n🔍 Testing simple prompt...")
    
    simple_prompt = "What is 2 + 2? Answer with just the number."
    
    try:
        start_time = time.time()
        response = llm_router.invoke(simple_prompt)
        response_time = time.time() - start_time
        
        print(f"✅ Simple prompt response: {response}")
        print(f"⏱️  Response time: {response_time:.2f}s")
        return True, response_time, str(response)
    except Exception as e:
        print(f"❌ Simple prompt failed: {str(e)}")
        return False, 0, ""

def test_stock_analysis_prompt():
    """Test stock analysis style prompt"""
    print("\n🔍 Testing stock analysis prompt...")
    
    analysis_prompt = """
    Analyze VNM stock in Vietnam market. Provide:
    1. Technical analysis summary (RSI, MACD, moving averages)
    2. Market sentiment analysis
    3. Risk assessment
    4. Investment recommendation (BUY/SELL/HOLD)
    
    Keep response under 200 words.
    """
    
    try:
        start_time = time.time()
        response = llm_router.invoke(analysis_prompt)
        response_time = time.time() - start_time
        
        print(f"✅ Analysis prompt response length: {len(str(response))} chars")
        print(f"⏱️  Response time: {response_time:.2f}s")
        return True, response_time, str(response)
    except Exception as e:
        print(f"❌ Analysis prompt failed: {str(e)}")
        return False, 0, ""

def test_multi_agent_simulation():
    """Simulate multi-agent workflow"""
    print("\n🔍 Testing multi-agent simulation...")
    
    agents = [
        ("Planner", "Create analysis plan for VNM stock with swing trading horizon"),
        ("Market", "Analyze Vietnam market conditions for VNM stock"),
        ("Technical", "Analyze technical indicators for VNM stock"),
        ("News", "Analyze recent news sentiment for VNM stock"),
        ("Risk", "Assess risk factors for VNM stock"),
        ("Decision", "Make final investment decision for VNM stock")
    ]
    
    total_time = 0
    results = []
    
    for agent_name, prompt in agents:
        try:
            start_time = time.time()
            response = llm_router.invoke(prompt)
            agent_time = time.time() - start_time
            total_time += agent_time
            
            results.append({
                'agent': agent_name,
                'time': agent_time,
                'response_length': len(str(response))
            })
            
            print(f"  ✅ {agent_name}: {agent_time:.2f}s ({len(str(response))} chars)")
            
        except Exception as e:
            print(f"  ❌ {agent_name}: {str(e)}")
            results.append({
                'agent': agent_name,
                'time': 0,
                'error': str(e)
            })
    
    print(f"\n📊 Multi-agent total time: {total_time:.2f}s")
    return results, total_time

def test_concurrent_requests():
    """Test concurrent request handling"""
    print("\n🔍 Testing concurrent requests...")
    
    import threading
    import queue
    
    def worker(prompt, result_queue):
        try:
            start_time = time.time()
            response = llm_router.invoke(prompt)
            end_time = time.time()
            result_queue.put({
                'success': True,
                'time': end_time - start_time,
                'response': str(response)
            })
        except Exception as e:
            result_queue.put({
                'success': False,
                'error': str(e)
            })
    
    # Test 3 concurrent requests
    prompts = [
        "What is the current stock market trend?",
        "Analyze technical indicators for FPT stock",
        "What are the risk factors in Vietnam market?"
    ]
    
    threads = []
    result_queue = queue.Queue()
    
    start_time = time.time()
    
    for prompt in prompts:
        thread = threading.Thread(target=worker, args=(prompt, result_queue))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    
    # Collect results
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    successful = [r for r in results if r['success']]
    
    print(f"✅ Concurrent requests: {len(successful)}/{len(prompts)} successful")
    print(f"⏱️  Total time: {total_time:.2f}s")
    
    if successful:
        avg_time = sum(r['time'] for r in successful) / len(successful)
        print(f"⏱️  Average response time: {avg_time:.2f}s")
    
    return results, total_time

def main():
    """Main test function"""
    print("🚀 Vietnam Stock Analyzer - Ollama Performance Test")
    print("=" * 60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Connection
    connection_ok, connection_time = test_ollama_connection()
    if not connection_ok:
        print("\n❌ Cannot proceed - Ollama connection failed")
        return
    
    # Test 2: Simple prompt
    simple_ok, simple_time, simple_response = test_simple_prompt()
    
    # Test 3: Analysis prompt
    analysis_ok, analysis_time, analysis_response = test_stock_analysis_prompt()
    
    # Test 4: Multi-agent simulation
    agent_results, agent_total_time = test_multi_agent_simulation()
    
    # Test 5: Concurrent requests
    concurrent_results, concurrent_total_time = test_concurrent_requests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"🔌 Connection time: {connection_time:.2f}s")
    
    if simple_ok:
        print(f"📝 Simple prompt: {simple_time:.2f}s")
    
    if analysis_ok:
        print(f"📈 Analysis prompt: {analysis_time:.2f}s")
    
    print(f"🤖 Multi-agent total: {agent_total_time:.2f}s")
    print(f"⚡ Concurrent total: {concurrent_total_time:.2f}s")
    
    # Analysis
    print("\n🔍 PERFORMANCE ANALYSIS")
    print("-" * 40)
    
    if simple_ok and analysis_ok:
        complexity_factor = analysis_time / simple_time if simple_time > 0 else 0
        print(f"📊 Complexity factor: {complexity_factor:.1f}x")
        
        if complexity_factor > 5:
            print("⚠️  High complexity factor - prompts may be too complex")
        elif complexity_factor > 2:
            print("⚠️  Moderate complexity factor")
        else:
            print("✅ Reasonable complexity factor")
    
    if agent_results:
        avg_agent_time = sum(r['time'] for r in agent_results if 'time' in r) / len([r for r in agent_results if 'time' in r])
        print(f"📈 Average agent time: {avg_agent_time:.2f}s")
        
        if avg_agent_time > 10:
            print("⚠️  Slow agent responses - consider optimization")
        elif avg_agent_time > 5:
            print("⚠️  Moderate agent speed")
        else:
            print("✅ Good agent speed")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 40)
    
    if simple_time > 5:
        print("🔧 Simple responses are slow - check Ollama model and resources")
    
    if agent_total_time > 60:
        print("🔧 Multi-agent analysis is very slow - consider:")
        print("   • Using smaller model (phi3, qwen:7b)")
        print("   • Reducing prompt complexity")
        print("   • Implementing response caching")
        print("   • Using concurrent processing")
    
    if concurrent_total_time > agent_total_time * 0.7:
        print("🔧 Concurrent processing shows good performance")
    else:
        print("🔧 Consider implementing concurrent processing")
    
    print(f"\n✅ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
