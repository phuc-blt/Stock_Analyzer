from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.graph import build_graph
from app.services.market_data import fetch_vietnam_stock_data, get_vietnam_stock_list
from app.services.news_sentiment import (
    get_vietnam_market_sentiment,
    analyze_vietnam_stock_news
)
from app.services.indicators import calculate_vietnam_indicators
import traceback
import pandas as pd
import asyncio
import time
import uuid
from functools import lru_cache

app = FastAPI(
    title="Vietnam Stock Multi-Agent Analyzer",
    description="Multi-agent system for Vietnam stock market analysis using AI",
    version="2.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Global objects
# -----------------------------
graph = None
analysis_jobs: Dict[str, Dict[str, Any]] = {}

# -----------------------------
# Startup
# -----------------------------
@app.on_event("startup")
async def startup_event():
    global graph
    try:
        print("Building graph...")
        start = time.time()
        graph = await asyncio.to_thread(build_graph)
        print(f"Graph ready in {time.time() - start:.2f}s")
    except Exception as e:
        print(f"Error building graph: {e}")
        graph = None


# -----------------------------
# Helpers
# -----------------------------
def serialize_analysis_data(data: Any) -> Any:
    """Convert non-serializable objects to JSON-safe structures."""
    if isinstance(data, pd.DataFrame):
        return data.tail(200).to_dict("records")
    elif isinstance(data, pd.Series):
        return data.to_dict()
    elif isinstance(data, dict):
        return {k: serialize_analysis_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_analysis_data(v) for v in data]
    elif hasattr(data, "__dict__"):
        try:
            return serialize_analysis_data(data.__dict__)
        except:
            return str(data)
    return data


@lru_cache(maxsize=200)
def cached_stock_data(ticker: str):
    return fetch_vietnam_stock_data(ticker)


# -----------------------------
# Models
# -----------------------------
class AnalyzeRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    horizon: str = Field(default="swing")
    risk_tolerance: str = Field(default="medium")


class QuickAnalysisRequest(BaseModel):
    ticker: str


class MarketSentimentRequest(BaseModel):
    timeframe: str = Field(default="current")


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


# -----------------------------
# Health
# -----------------------------
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "graph_status": "ready" if graph else "error"
    }


# -----------------------------
# Background Analysis Worker
# -----------------------------
async def run_analysis_job(job_id: str, req: AnalyzeRequest):
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

        result = await asyncio.wait_for(
            asyncio.to_thread(graph.invoke, initial_state),
            timeout=120
        )

        serialized_analysis = serialize_analysis_data({
            "plan": result.get("plan", {}),
            "market_analysis": result.get("market_data", {}),
            "technical_analysis": result.get("technical_data", {}),
            "news_analysis": result.get("news_data", {}),
            "risk_analysis": result.get("risk_data", {}),
            "final_decision": result.get("final_decision", {})
        })

        analysis_jobs[job_id] = {
            "status": "completed",
            "result": {
                "success": True,
                "ticker": req.ticker.upper(),
                "horizon": req.horizon,
                "timestamp": datetime.now().isoformat(),
                "analysis": serialized_analysis
            }
        }

    except asyncio.TimeoutError:
        analysis_jobs[job_id] = {
            "status": "failed",
            "result": {
                "success": False,
                "error": "Analysis timeout after 120 seconds"
            }
        }

    except Exception as e:
        analysis_jobs[job_id] = {
            "status": "failed",
            "result": {
                "success": False,
                "error": str(e)
            }
        }


# -----------------------------
# Main Analyze (async job)
# -----------------------------
@app.post("/api/v2/analyze")
async def analyze_stock(req: AnalyzeRequest, background_tasks: BackgroundTasks):
    if not graph:
        raise HTTPException(status_code=503, detail="Analysis service unavailable")

    job_id = str(uuid.uuid4())

    analysis_jobs[job_id] = {
        "status": "processing",
        "created_at": datetime.now().isoformat()
    }

    background_tasks.add_task(run_analysis_job, job_id, req)

    return {
        "success": True,
        "job_id": job_id,
        "status": "processing",
        "message": "Analysis started"
    }


# -----------------------------
# Job Status
# -----------------------------
@app.get("/api/v2/analyze/{job_id}")
async def get_analysis_result(job_id: str):
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return analysis_jobs[job_id]


# -----------------------------
# Quick Analyze
# -----------------------------
@app.post("/api/v1/quick-analyze", response_model=QuickAnalysisResponse)
async def quick_analyze_stock(req: QuickAnalysisRequest):
    try:
        market_data = await asyncio.wait_for(
            asyncio.to_thread(cached_stock_data, req.ticker.upper()),
            timeout=20
        )

        technical_data = await asyncio.wait_for(
            asyncio.to_thread(
                calculate_vietnam_indicators,
                market_data.get("history", {})
            ),
            timeout=20
        )

        news_data = await asyncio.wait_for(
            asyncio.to_thread(
                analyze_vietnam_stock_news,
                req.ticker.upper()
            ),
            timeout=20
        )

        tech_signal = "HOLD"

        rsi = technical_data.get("rsi", 50)
        macd = technical_data.get("macd", 0)

        if rsi < 35 and macd > 0:
            tech_signal = "BUY"
        elif rsi > 70:
            tech_signal = "SELL"

        recommendation = tech_signal
        confidence = 60

        if news_data.get("sentiment") == "POSITIVE" and tech_signal != "SELL":
            if tech_signal == "HOLD":
                recommendation = "BUY"
            confidence = min(confidence + 15, 90)

        elif news_data.get("sentiment") == "NEGATIVE":
            if tech_signal == "BUY":
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
                "rsi": rsi,
                "macd": macd,
                "ma20": technical_data.get("ma20", 0),
                "ma50": technical_data.get("ma50", 0),
                "volume_ratio": technical_data.get("volume_ratio", 1),
                "sentiment": news_data.get("sentiment", "NEUTRAL"),
                "sentiment_score": news_data.get("sentiment_score", 0),
                "pe_ratio": market_data.get("pe_ratio", 0),
            }
        )

    except Exception as e:
        return QuickAnalysisResponse(
            success=False,
            ticker=req.ticker.upper(),
            company_name="",
            current_price=0,
            recommendation="HOLD",
            confidence=0,
            key_signals={},
            error=str(e)
        )


# -----------------------------
# Stock List (parallel fetch)
# -----------------------------
@app.get("/api/v1/stocks", response_model=StockListResponse)
async def get_vietnam_stocks():
    try:
        stocks = await asyncio.to_thread(get_vietnam_stock_list)

        async def fetch_stock(stock):
            try:
                market_data = await asyncio.wait_for(
                    asyncio.to_thread(
                        cached_stock_data,
                        stock["ticker"]
                    ),
                    timeout=15
                )

                return {
                    **stock,
                    "current_price": market_data.get("price", 0),
                    "pe_ratio": market_data.get("pe_ratio", 0),
                    "market_cap": market_data.get("market_cap", 0),
                    "volume": market_data.get("volume", 0),
                }

            except:
                return {
                    **stock,
                    "current_price": 0,
                    "pe_ratio": 0,
                    "market_cap": 0,
                    "volume": 0,
                }

        tasks = [fetch_stock(stock) for stock in stocks]
        stocks_with_prices = await asyncio.gather(*tasks)

        return StockListResponse(
            success=True,
            stocks=stocks_with_prices,
            count=len(stocks_with_prices)
        )

    except Exception:
        return StockListResponse(
            success=False,
            stocks=[],
            count=0
        )

# -----------------------------
# Market Sentiment
# -----------------------------
@app.get("/api/v1/market-sentiment", response_model=MarketSentimentResponse)
async def get_market_sentiment():
    """
    Get overall market sentiment analysis
    """
    try:
        # This would integrate with a real market sentiment API
        sentiment_data = {
            "overall": "neutral",
            "score": 0.5,
            "factors": [
                "Market volatility within normal range",
                "Mixed signals from technical indicators",
                "Awaiting key economic data releases"
            ],
        }

        return {
            "success": True,
            "ticker": ticker.upper(),
            "data": response_data,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "success": False,
            "ticker": ticker.upper(),
            "data": {},
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# -----------------------------
# Root
# -----------------------------
@app.get("/")
async def root():
    return {
        "message": "Vietnam Stock Multi-Agent Analyzer API",
        "version": "2.0.0",
        "features": [
            "Async processing",
            "Background jobs",
            "Timeout protection",
            "Parallel stock fetching",
            "Caching",
            "Reduced blocking"
        ],
        "endpoints": {
            "health": "/health",
            "analyze_start": "/api/v2/analyze",
            "analyze_result": "/api/v2/analyze/{job_id}",
            "quick_analyze": "/api/v1/quick-analyze",
            "stocks": "/api/v1/stocks",
            "market_sentiment": "/api/v1/market-sentiment",
            "stock_data": "/api/v1/stock/{ticker}/data",
            "chat": "/api/v1/chat"
        }
    }

# -----------------------------
# Chat Analysis
# -----------------------------
class ChatRequest(BaseModel):
    ticker: str
    message: str

class ChatResponse(BaseModel):
    success: bool
    ticker: str
    response: str
    timestamp: str

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_analysis(req: ChatRequest):
    """
    AI-powered chat analysis for stock questions
    """
    try:
        ticker = req.ticker.upper()
        user_message = req.message.lower()
        
        # Generate contextual response based on user question
        response = generate_contextual_response(ticker, user_message)
        
        return ChatResponse(
            success=True,
            ticker=ticker,
            response=response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        error_msg = f"Chat analysis failed: {str(e)}"
        print(f"Error in chat analysis: {error_msg}")
        return ChatResponse(
            success=False,
            ticker=req.ticker.upper(),
            response="Xin lỗi, có lỗi xảy ra khi phân tích. Vui lòng thử lại sau.",
            timestamp=datetime.now().isoformat()
        )

def generate_contextual_response(ticker: str, message: str) -> str:
    """
    Generate contextual response based on user question
    """
    # Simple mock data for testing
    current_price = 60000
    rsi = 45
    sentiment = "neutral"
    change_percent = 1.5
    
    # Analyze user intent
    if "mua" in message or "buy" in message or "nên mua" in message:
        return generate_buy_recommendation(ticker, current_price, rsi, sentiment, change_percent)
    elif "bán" in message or "sell" in message or "nên bán" in message:
        return generate_sell_recommendation(ticker, current_price, rsi, sentiment, change_percent)
    elif "giá" in message or "price" in message:
        return generate_price_analysis(ticker, current_price, change_percent)
    elif "kỹ thuật" in message or "technical" in message or "rsi" in message:
        return generate_technical_analysis(ticker, rsi)
    elif "tin tức" in message or "news" in message or "tình cảm" in message:
        return generate_news_analysis(ticker, sentiment)
    elif "dự đoán" in message or "predict" in message or "xu hướng" in message:
        return generate_prediction(ticker, current_price, rsi, sentiment, change_percent)
    else:
        return generate_general_analysis(ticker, current_price, rsi, sentiment, change_percent)

def generate_buy_recommendation(ticker: str, price: float, rsi: float, sentiment: str, change_percent: float) -> str:
    """Generate buy recommendation"""
    reasons = []
    
    if rsi < 30:
        reasons.append(f"RSI ({rsi:.1f}) cho thấy cổ phiếu đang ở vùng quá bán, là dấu hiệu mua tốt")
    elif rsi < 50:
        reasons.append(f"RSI ({rsi:.1f}) ở mức hợp lý, không quá đắt")
    
    if sentiment == "positive":
        reasons.append("Tin tức gần đây có xu hướng tích cực")
    elif sentiment == "neutral":
        reasons.append("Tin tức trung lập, không có rủi ro lớn")
    
    if change_percent < -2:
        reasons.append(f"Giá đã giảm {abs(change_percent):.2f}%, có thể là cơ hội mua giá tốt")
    
    if not reasons:
        reasons.append("Các chỉ báo kỹ thuật và tin tức không cho thấy rủi ro lớn")
    
    recommendation = "MUA" if len(reasons) >= 2 else "XEM XÉT"
    
    response = f"## Phân Tích Khuyến Nghị Mua {ticker}\n\n"
    response += f"**Khuyến nghị:** {recommendation}\n\n"
    response += f"**Giá hiện tại:** {price:,.0f}đ\n\n"
    response += "**Lý do:**\n"
    for i, reason in enumerate(reasons, 1):
        response += f"{i}. {reason}\n"
    
    response += f"\n**Mức độ tin cậy:** {70 if len(reasons) >= 2 else 50}%\n"
    response += f"\n*Lưu ý: Đây là phân tích dựa trên dữ liệu kỹ thuật và tin tức hiện tại. Hãy luôn tự nghiên cứu trước khi quyết định đầu tư.*"
    
    return response

def generate_sell_recommendation(ticker: str, price: float, rsi: float, sentiment: str, change_percent: float) -> str:
    """Generate sell recommendation"""
    reasons = []
    
    if rsi > 70:
        reasons.append(f"RSI ({rsi:.1f}) cho thấy cổ phiếu đang ở vùng quá mua, có thể điều chỉnh")
    elif rsi > 60:
        reasons.append(f"RSI ({rsi:.1f}) ở mức cao, cần cân nhắc chốt lời")
    
    if sentiment == "negative":
        reasons.append("Tin tức gần đây có xu hướng tiêu cực")
    
    if change_percent > 3:
        reasons.append(f"Giá đã tăng {change_percent:.2f}%, có thể là thời điểm tốt để chốt lời")
    
    if not reasons:
        reasons.append("Các chỉ báo không cho thấy tín hiệu bán rõ ràng")
    
    recommendation = "BÁN" if len(reasons) >= 2 else "GIỮ"
    
    response = f"## Phân Tích Khuyến Nghị Bán {ticker}\n\n"
    response += f"**Khuyến nghị:** {recommendation}\n\n"
    response += f"**Giá hiện tại:** {price:,.0f}đ\n\n"
    response += "**Lý do:**\n"
    for i, reason in enumerate(reasons, 1):
        response += f"{i}. {reason}\n"
    
    response += f"\n**Mức độ tin cậy:** {70 if len(reasons) >= 2 else 50}%\n"
    response += f"\n*Lưu ý: Đây là phân tích dựa trên dữ liệu kỹ thuật và tin tức hiện tại. Hãy luôn tự nghiên cứu trước khi quyết định đầu tư.*"
    
    return response

def generate_price_analysis(ticker: str, price: float, change_percent: float) -> str:
    """Generate price analysis"""
    trend = "tăng" if change_percent > 0 else "giảm" if change_percent < 0 else "đứng"
    
    response = f"## Phân Tích Giá {ticker}\n\n"
    response += f"**Giá hiện tại:** {price:,.0f}đ\n"
    response += f"**Thay đổi:** {trend} {abs(change_percent):.2f}%\n\n"
    
    if change_percent > 2:
        response += "**Phân tích:** Giá đang tăng mạnh, có thể do tin tức tích cực hoặc dòng tiền vào.\n"
    elif change_percent < -2:
        response += "**Phân tích:** Giá đang giảm mạnh, có thể do tin tức tiêu cực hoặc dòng tiền rút ra.\n"
    else:
        response += "**Phân tích:** Giá đang biến động trong biên độ hẹp, thị trường đang chờ đợi tín hiệu mới.\n"
    
    response += f"\n**Khuyến nghị:** {'Xem xét mua nếu có tin tức tốt' if trend == 'giảm' else 'Cân nhắc chốt lời một phần' if trend == 'tăng' else 'Giữ nguyên vị thế'}\n"
    
    return response

def generate_technical_analysis(ticker: str, rsi: float) -> str:
    """Generate technical analysis"""
    response = f"## Phân Tích Kỹ Thuật {ticker}\n\n"
    response += f"**RSI:** {rsi:.1f} "
    if rsi > 70:
        response += "(Quá mua - Cẩn thận)"
    elif rsi < 30:
        response += "(Quá bán - Cơ hội mua)"
    else:
        response += "(Bình thường)"
    
    response += f"\n**MACD:** 55.2\n"
    response += f"**MA20:** 59,485đ\n"
    response += f"**MA50:** 60,458đ\n\n"
    
    response += "**Xu hướng:** Tăng giá ngắn hạn (MA20 > MA50)\n"
    response += f"\n**Tín hiệu:** {'MUA' if rsi < 35 else 'BÁN' if rsi > 65 else 'GIỮ'}\n"
    
    return response

def generate_news_analysis(ticker: str, sentiment: str) -> str:
    """Generate news analysis"""
    response = f"## Phân Tích Tin Tức {ticker}\n\n"
    response += f"**Tình cảm thị trường:** {sentiment.upper()}\n"
    response += f"**Score:** 0.08\n\n"
    
    if sentiment == "positive":
        response += "**Phân tích:** Tin tức gần đây có xu hướng tích cực, có thể hỗ trợ giá cổ phiếu.\n"
        response += "**Khuyến nghị:** Cân nhắc tích cơ hội khi giá điều chỉnh.\n"
    elif sentiment == "negative":
        response += "**Phân tích:** Tin tức gần đây có xu hướng tiêu cực, có thể ảnh hưởng tiêu cực đến giá.\n"
        response += "**Khuyến nghị:** Thận trọng, có thể chờ đợi tin tức tốt hơn.\n"
    else:
        response += "**Phân tích:** Tin tức trung lập, không có tín hiệu rõ ràng từ tin tức.\n"
        response += "**Khuyến nghị:** Dựa vào phân tích kỹ thuật chính.\n"
    
    return response

def generate_prediction(ticker: str, price: float, rsi: float, sentiment: str, change_percent: float) -> str:
    """Generate prediction"""
    response = f"## Dự Đoán Xu Hướng {ticker}\n\n"
    response += f"**Giá hiện tại:** {price:,.0f}đ\n"
    response += f"**RSI:** {rsi:.1f}\n"
    response += f"**Tình cảm tin tức:** {sentiment}\n\n"
    
    factors = []
    if rsi < 35:
        factors.append("RSI thấp cho thấy khả năng phục hồi")
    elif rsi > 65:
        factors.append("RSI cao cho thấy khả năng điều chỉnh")
    
    if sentiment == "positive":
        factors.append("Tin tức tích cực hỗ trợ giá")
    elif sentiment == "negative":
        factors.append("Tin tức tiêu cực có thể ảnh hưởng")
    
    if change_percent > 2:
        factors.append("Giá tăng mạnh có thể cần điều chỉnh")
    elif change_percent < -2:
        factors.append("Giá giảm mạnh có thể phục hồi")
    
    if not factors:
        factors.append("Các chỉ báo kỹ thuật đang ở mức trung bình")
    
    response += "**Các yếu tố ảnh hưởng:**\n"
    for i, factor in enumerate(factors, 1):
        response += f"{i}. {factor}\n"
    
    # Overall prediction
    if len(factors) >= 2:
        prediction = "XU HƯỚNG TĂNG (ngắn hạn)"
    elif len(factors) == 1 and "tiêu cực" in factors[0]:
        prediction = "XU HƯỚNG GIẢM (ngắn hạn)"
    else:
        prediction = "ĐỨNG GIÁ / BIẾN ĐỘNG NHỎ"
    
    response += f"\n**Dự đoán:** {prediction}\n"
    response += f"\n*Đây là dự đoán dựa trên dữ liệu hiện tại và không đảm bảo chính xác 100%.*"
    
    return response

def generate_general_analysis(ticker: str, price: float, rsi: float, sentiment: str, change_percent: float) -> str:
    """Generate general analysis"""
    response = f"## Phân Tích Tổng Quan {ticker}\n\n"
    response += f"**Giá hiện tại:** {price:,.0f}đ\n"
    response += f"**Thay đổi:** {change_percent:+.2f}%\n\n"
    
    response += "**Phân tích kỹ thuật:**\n"
    response += f"- RSI: {rsi:.1f}\n"
    response += f"- MACD: 55.2\n\n"
    
    response += "**Tình cảm tin tức:**\n"
    response += f"- Sentiment: {sentiment}\n"
    response += f"- Score: 0.08\n\n"
    
    response += "**Tổng quan:** Cổ phiếu đang "
    if change_percent > 0:
        response += "tăng giá"
    elif change_percent < 0:
        response += "giảm giá"
    else:
        response += "đứng giá"
    
    response += f" với các chỉ báo kỹ thuật {'tốt' if rsi < 70 else 'cần chú ý'} "
    response += f"và tin tức {'tích cực' if sentiment == 'positive' else 'tiêu cực' if sentiment == 'negative' else 'trung lập'}.\n\n"
    
    response += "**Khuyến nghị:** Hãy tiếp tục theo dõi và đặt câu hỏi cụ thể hơn để nhận phân tích chi tiết."
    
    return response