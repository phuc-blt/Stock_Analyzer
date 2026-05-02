"""
Simple FastAPI backend for testing - no blocking operations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import traceback

app = FastAPI(
    title="Vietnam Stock Multi-Agent Analyzer",
    description="Multi-agent system for Vietnam stock market analysis using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://26.237.224.250:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "graph_status": "simple_mode"
    }

# Simple stock list endpoint
@app.get("/api/v1/stocks")
def get_vietnam_stocks():
    """Simple stock list without external API calls"""
    try:
        # Static data for testing
        stocks = [
            {
                "ticker": "VNM",
                "name": "Vinamilk",
                "sector": "Thực phẩm & Đồ uống",
                "current_price": 60900.0,
                "pe_ratio": 15.128593,
                "market_cap": 127278285586432,
                "volume": 2582460
            },
            {
                "ticker": "FPT",
                "name": "FPT Corporation",
                "sector": "Công nghệ thông tin",
                "current_price": 92500.0,
                "pe_ratio": 18.456789,
                "market_cap": 98765432100000,
                "volume": 1234567
            },
            {
                "ticker": "VCB",
                "name": "Vietcombank",
                "sector": "Ngân hàng",
                "current_price": 45200.0,
                "pe_ratio": 12.345678,
                "market_cap": 87654321000000,
                "volume": 987654
            }
        ]
        
        return {
            "success": True,
            "stocks": stocks,
            "count": len(stocks)
        }
        
    except Exception as e:
        error_msg = f"Failed to get stock list: {str(e)}"
        print(f"Error getting stock list: {error_msg}")
        
        return {
            "success": False,
            "stocks": [],
            "count": 0
        }

# Simple market sentiment endpoint
@app.post("/api/v1/market-sentiment")
def get_market_sentiment():
    """Simple market sentiment without external API calls"""
    try:
        # Static sentiment data for testing
        sentiment_data = {
            "overall_sentiment": "NEUTRAL",
            "sentiment_score": 0.05,
            "market_trend": "SIDEWAYS",
            "confidence": 65,
            "key_factors": [
                "Market stability",
                "Mixed earnings reports",
                "Global uncertainty"
            ],
            "last_updated": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "sentiment": sentiment_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_msg = f"Failed to get market sentiment: {str(e)}"
        print(f"Error getting market sentiment: {error_msg}")
        
        return {
            "success": False,
            "sentiment": {},
            "timestamp": datetime.now().isoformat()
        }

# Simple quick analysis endpoint
@app.post("/api/v1/quick-analyze")
def quick_analyze_stock():
    """Simple quick analysis without external API calls"""
    try:
        # Static analysis data for testing
        analysis_data = {
            "ticker": "VNM",
            "company_name": "Vinamilk",
            "current_price": 60900.0,
            "recommendation": "HOLD",
            "confidence": 60,
            "key_signals": {
                "rsi": 45.5,
                "macd": -123.45,
                "ma20": 61000.0,
                "ma50": 60800.0,
                "sentiment": "NEUTRAL",
                "sentiment_score": 0.05,
                "volume_ratio": 1.2,
                "pe_ratio": 15.128593
            }
        }
        
        return {
            "success": True,
            **analysis_data
        }
        
    except Exception as e:
        error_msg = f"Quick analysis failed: {str(e)}"
        print(f"Error in quick analysis: {error_msg}")
        
        return {
            "success": False,
            "ticker": "UNKNOWN",
            "company_name": "",
            "current_price": 0,
            "recommendation": "HOLD",
            "confidence": 0,
            "key_signals": {},
            "error": error_msg
        }

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Vietnam Stock Multi-Agent Analyzer API - Simple Mode",
        "version": "1.0.0",
        "mode": "simple_testing",
        "endpoints": {
            "health": "/health",
            "quick_analyze": "/api/v1/quick-analyze",
            "stocks": "/api/v1/stocks",
            "market_sentiment": "/api/v1/market-sentiment"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
