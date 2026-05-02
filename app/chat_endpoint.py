# Simple chat endpoint for testing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import asyncio

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
