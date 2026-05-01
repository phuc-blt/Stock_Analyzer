from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.graph import build_graph
from app.services.market_data import fetch_vietnam_stock_data, get_vietnam_stock_list
from app.services.news_sentiment import get_vietnam_market_sentiment
import traceback
import pandas as pd

app = FastAPI(
    title="Vietnam Stock Multi-Agent Analyzer",
    description="Multi-agent system for Vietnam stock market analysis using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Helper function to handle serialization of non-serializable objects
def serialize_analysis_data(data: Any) -> Any:
    """Convert non-serializable objects to serializable formats"""
    if isinstance(data, pd.DataFrame):
        return data.to_dict('records')
    elif isinstance(data, pd.Series):
        return data.to_dict()
    elif isinstance(data, dict):
        return {k: serialize_analysis_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_analysis_data(item) for item in data]
    elif hasattr(data, '__dict__'):
        # For custom objects, try to serialize their attributes
        try:
            return serialize_analysis_data(data.__dict__)
        except:
            return str(data)
    else:
        return data

# Initialize the multi-agent graph
try:
    graph = build_graph()
except Exception as e:
    print(f"Error building graph: {e}")
    graph = None


# Pydantic models for API
class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g., VNM, FPT, VCB)")
    horizon: str = Field(default="swing", description="Investment horizon: short_term, swing, long_term")
    risk_tolerance: str = Field(default="medium", description="Risk tolerance: low, medium, high")


class QuickAnalysisRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")


class MarketSentimentRequest(BaseModel):
    timeframe: str = Field(default="current", description="Timeframe for sentiment analysis")


# Response models
class AnalysisResponse(BaseModel):
    success: bool
    ticker: str
    horizon: str
    timestamp: str
    analysis: Dict[str, Any]
    error: Optional[str] = None


class QuickAnalysisResponse(BaseModel):
    success: bool
    ticker: str
    company_name: str
    current_price: float
    recommendation: str
    confidence: int
    key_signals: Dict[str, Any]
    error: Optional[str] = None


class StockListResponse(BaseModel):
    success: bool
    stocks: List[Dict[str, Any]]
    count: int


class MarketSentimentResponse(BaseModel):
    success: bool
    sentiment: Dict[str, Any]
    timestamp: str


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "graph_status": "ready" if graph else "error"
    }


# Main analysis endpoint
@app.post("/api/v1/analyze", response_model=AnalysisResponse)
def analyze_stock(req: AnalyzeRequest):
    """
    Comprehensive multi-agent analysis of Vietnam stock
    """
    if not graph:
        raise HTTPException(status_code=503, detail="Analysis service not available")
    
    try:
        initial_state = {
            "ticker": req.ticker.upper(),
            "horizon": req.horizon,
            "risk_tolerance": req.risk_tolerance,
            "timestamp": datetime.now().isoformat(),
            "tasks": [],
            "plan": {},
            "market_data": {},
            "technical_data": {},
            "news_data": {},
            "risk_data": {},
            "final_decision": {}
        }

        result = graph.invoke(initial_state)

        # Serialize the analysis data to handle DataFrames and other non-serializable objects
        serialized_analysis = serialize_analysis_data({
            "plan": result.get("plan", {}),
            "market_analysis": result.get("market_data", {}),
            "technical_analysis": result.get("technical_data", {}),
            "news_analysis": result.get("news_data", {}),
            "risk_analysis": result.get("risk_data", {}),
            "final_decision": result.get("final_decision", {})
        })

        return AnalysisResponse(
            success=True,
            ticker=result["ticker"],
            horizon=result["horizon"],
            timestamp=result.get("timestamp", datetime.now().isoformat()),
            analysis=serialized_analysis
        )

    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        print(f"Error in analysis: {error_msg}")
        print(traceback.format_exc())
        
        return AnalysisResponse(
            success=False,
            ticker=req.ticker.upper(),
            horizon=req.horizon,
            timestamp=datetime.now().isoformat(),
            analysis={},
            error=error_msg
        )


# Quick analysis endpoint for frontend
@app.post("/api/v1/quick-analyze", response_model=QuickAnalysisResponse)
def quick_analyze_stock(req: QuickAnalysisRequest):
    """
    Quick analysis for frontend display
    """
    try:
        # Get basic market data
        market_data = fetch_vietnam_stock_data(req.ticker.upper())
        
        # Get quick technical and sentiment data
        from app.services.indicators import calculate_vietnam_indicators
        from app.services.news_sentiment import analyze_vietnam_stock_news
        
        technical_data = calculate_vietnam_indicators(market_data.get("history", {}))
        news_data = analyze_vietnam_stock_news(req.ticker.upper())
        
        # Simple decision logic
        tech_signal = "HOLD"
        if technical_data.get("rsi", 50) < 35 and technical_data.get("macd", 0) > 0:
            tech_signal = "BUY"
        elif technical_data.get("rsi", 50) > 70:
            tech_signal = "SELL"
        
        recommendation = tech_signal
        confidence = 60
        
        # Adjust based on news sentiment
        if news_data.get("sentiment") == "POSITIVE" and tech_signal != "SELL":
            if tech_signal == "HOLD":
                recommendation = "BUY"
            confidence = min(confidence + 15, 85)
        elif news_data.get("sentiment") == "NEGATIVE" and tech_signal == "BUY":
            recommendation = "HOLD"
            confidence = max(confidence - 20, 30)
        
        return QuickAnalysisResponse(
            success=True,
            ticker=req.ticker.upper(),
            company_name=market_data.get("company_name", ""),
            current_price=market_data.get("price", 0),
            recommendation=recommendation,
            confidence=confidence,
            key_signals={
                "rsi": technical_data.get("rsi", 50),
                "macd": technical_data.get("macd", 0),
                "ma20": technical_data.get("ma20", 0),
                "ma50": technical_data.get("ma50", 0),
                "sentiment": news_data.get("sentiment", "NEUTRAL"),
                "sentiment_score": news_data.get("sentiment_score", 0),
                "volume_ratio": technical_data.get("volume_ratio", 1),
                "pe_ratio": market_data.get("pe_ratio", 0)
            }
        )

    except Exception as e:
        error_msg = f"Quick analysis failed: {str(e)}"
        print(f"Error in quick analysis: {error_msg}")
        
        return QuickAnalysisResponse(
            success=False,
            ticker=req.ticker.upper(),
            company_name="",
            current_price=0,
            recommendation="HOLD",
            confidence=0,
            key_signals={},
            error=error_msg
        )


# Get list of Vietnam stocks
@app.get("/api/v1/stocks", response_model=StockListResponse)
def get_vietnam_stocks():
    """
    Get list of popular Vietnam stocks for frontend
    """
    try:
        stocks = get_vietnam_stock_list()
        
        # Add current prices
        stocks_with_prices = []
        for stock in stocks:
            try:
                market_data = fetch_vietnam_stock_data(stock["ticker"])
                stocks_with_prices.append({
                    **stock,
                    "current_price": market_data.get("price", 0),
                    "pe_ratio": market_data.get("pe_ratio", 0),
                    "market_cap": market_data.get("market_cap", 0),
                    "volume": market_data.get("volume", 0)
                })
            except:
                stocks_with_prices.append({
                    **stock,
                    "current_price": 0,
                    "pe_ratio": 0,
                    "market_cap": 0,
                    "volume": 0
                })
        
        return StockListResponse(
            success=True,
            stocks=stocks_with_prices,
            count=len(stocks_with_prices)
        )

    except Exception as e:
        error_msg = f"Failed to get stock list: {str(e)}"
        print(f"Error getting stock list: {error_msg}")
        
        return StockListResponse(
            success=False,
            stocks=[],
            count=0
        )


# Get market sentiment
@app.post("/api/v1/market-sentiment", response_model=MarketSentimentResponse)
def get_market_sentiment(req: MarketSentimentRequest):
    """
    Get overall Vietnam market sentiment
    """
    try:
        sentiment_data = get_vietnam_market_sentiment()
        
        return MarketSentimentResponse(
            success=True,
            sentiment=sentiment_data,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        error_msg = f"Failed to get market sentiment: {str(e)}"
        print(f"Error getting market sentiment: {error_msg}")
        
        return MarketSentimentResponse(
            success=False,
            sentiment={},
            timestamp=datetime.now().isoformat()
        )


# Get detailed stock data
@app.get("/api/v1/stock/{ticker}/data")
def get_stock_data(ticker: str):
    """
    Get detailed market data for a specific stock
    """
    try:
        market_data = fetch_vietnam_stock_data(ticker.upper())
        
        # Remove history data for cleaner response
        response_data = {k: v for k, v in market_data.items() if k != "history"}
        
        return {
            "success": True,
            "ticker": ticker.upper(),
            "data": response_data,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        error_msg = f"Failed to get stock data: {str(e)}"
        print(f"Error getting stock data: {error_msg}")
        
        return {
            "success": False,
            "ticker": ticker.upper(),
            "data": {},
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }


# Legacy endpoints for backward compatibility
@app.post("/analyze")
def analyze_stock_legacy(req: AnalyzeRequest):
    """Legacy endpoint for backward compatibility"""
    return analyze_stock(req)


@app.get("/")
def root():
    return {
        "message": "Vietnam Stock Multi-Agent Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/v1/analyze",
            "quick_analyze": "/api/v1/quick-analyze",
            "stocks": "/api/v1/stocks",
            "market_sentiment": "/api/v1/market-sentiment",
            "stock_data": "/api/v1/stock/{ticker}/data"
        }
    }
