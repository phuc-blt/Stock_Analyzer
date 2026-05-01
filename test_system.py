#!/usr/bin/env python3
"""
Test script for Vietnam Stock Multi-Agent System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_components():
    """Test all system components"""
    print("🧪 Testing Vietnam Stock Multi-Agent System...")
    print("=" * 50)
    
    # Test 1: Graph building
    try:
        from app.graph import build_graph
        graph = build_graph()
        print("✅ Graph built successfully")
    except Exception as e:
        print(f"❌ Graph building failed: {e}")
        return False
    
    # Test 2: Market data
    try:
        from app.services.market_data import fetch_vietnam_stock_data
        data = fetch_vietnam_stock_data('VNM')
        print(f"✅ Market data: {data['ticker']} - {data['company_name']} - {data['price']} VND")
    except Exception as e:
        print(f"❌ Market data failed: {e}")
        return False
    
    # Test 3: Technical indicators
    try:
        from app.services.indicators import calculate_vietnam_indicators
        indicators = calculate_vietnam_indicators(data.get('history', {}))
        print(f"✅ Technical indicators: RSI={indicators.get('rsi', 'N/A')}, MACD={indicators.get('macd', 'N/A')}")
    except Exception as e:
        print(f"❌ Technical indicators failed: {e}")
        return False
    
    # Test 4: News sentiment
    try:
        from app.services.news_sentiment import analyze_vietnam_stock_news
        news = analyze_vietnam_stock_news('VNM')
        print(f"✅ News sentiment: {news.get('sentiment', 'N/A')} ({news.get('sentiment_score', 'N/A')})")
    except Exception as e:
        print(f"❌ News sentiment failed: {e}")
        return False
    
    # Test 5: Individual agents
    try:
        from app.agents.planner import PlannerAgent
        from app.agents.market import MarketAgent
        from app.agents.technical import TechnicalAgent
        from app.agents.news import NewsAgent
        from app.agents.risk import RiskAgent
        from app.agents.decision import DecisionAgent
        
        planner = PlannerAgent()
        market = MarketAgent()
        technical = TechnicalAgent()
        news = NewsAgent()
        risk = RiskAgent()
        decision = DecisionAgent()
        
        print("✅ All agents initialized successfully")
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False
    
    print("\n🎉 All components working correctly!")
    return True

def test_api_endpoints():
    """Test API endpoints structure"""
    print("\n🌐 Testing API structure...")
    
    try:
        from app.main import app
        routes = [route.path for route in app.routes]
        
        expected_routes = [
            "/health",
            "/api/v1/analyze",
            "/api/v1/quick-analyze", 
            "/api/v1/stocks",
            "/api/v1/market-sentiment",
            "/"
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ {route}")
            else:
                print(f"❌ Missing: {route}")
                return False
                
        print("✅ All API endpoints configured")
        return True
        
    except Exception as e:
        print(f"❌ API testing failed: {e}")
        return False

def test_full_workflow():
    """Test complete multi-agent workflow"""
    print("\n🔄 Testing complete workflow...")
    
    try:
        from app.graph import build_graph
        
        graph = build_graph()
        
        initial_state = {
            "ticker": "VNM",
            "horizon": "swing",
            "risk_tolerance": "medium",
            "timestamp": "2024-01-01T00:00:00",
            "tasks": [],
            "plan": {},
            "market_data": {},
            "technical_data": {},
            "news_data": {},
            "risk_data": {},
            "final_decision": {},
            "metadata": {}
        }
        
        # Run the workflow
        result = graph.invoke(initial_state)
        
        print(f"✅ Workflow completed for {result['ticker']}")
        print(f"✅ Recommendation: {result['final_decision'].get('recommendation', 'N/A')}")
        print(f"✅ Confidence: {result['final_decision'].get('confidence', 'N/A')}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = True
    
    # Run all tests
    success &= test_components()
    success &= test_api_endpoints()
    success &= test_full_workflow()
    
    if success:
        print("\n🚀 System ready for production!")
        print("\n📋 Available API endpoints:")
        print("   GET  /health - Health check")
        print("   POST /api/v1/analyze - Full multi-agent analysis")
        print("   POST /api/v1/quick-analyze - Quick analysis")
        print("   GET  /api/v1/stocks - List Vietnam stocks")
        print("   POST /api/v1/market-sentiment - Market sentiment")
        print("   GET  /api/v1/stock/{{ticker}}/data - Stock data")
        print("\n🔧 To start the server:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ System has issues - please check the errors above")
        sys.exit(1)
