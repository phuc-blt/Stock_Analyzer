import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random


def analyze_vietnam_stock_news(ticker: str) -> Dict[str, Any]:
    """
    Analyze news sentiment for Vietnam stock
    """
    try:
        # Try to get real news data (placeholder for actual news API integration)
        news_data = fetch_vietnam_stock_news(ticker)
        sentiment_analysis = analyze_sentiment(news_data)
        
        return {
            "ticker": ticker,
            "sentiment": sentiment_analysis["sentiment"],
            "sentiment_score": sentiment_analysis["score"],
            "news_count": len(news_data),
            "key_topics": sentiment_analysis["topics"],
            "recent_headlines": [item["title"] for item in news_data[:5]],
            "analysis_timestamp": datetime.now().isoformat(),
            "news_sources": list(set([item["source"] for item in news_data])),
            "detailed_analysis": sentiment_analysis
        }
        
    except Exception as e:
        print(f"Error analyzing news for {ticker}: {e}")
        return get_mock_news_sentiment(ticker)


def fetch_vietnam_stock_news(ticker: str) -> List[Dict[str, Any]]:
    """
    Fetch Vietnam stock news from various sources
    This is a placeholder - integrate with actual news APIs like:
    - CafeF API
    - Vietstock API  
    - NewsAPI with Vietnam-specific filters
    - Financial news aggregators
    """
    # Mock news data for development
    mock_news = get_mock_news_data(ticker)
    return mock_news


def analyze_sentiment(news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze sentiment from news data
    """
    if not news_data:
        return {
            "sentiment": "NEUTRAL",
            "score": 0.0,
            "topics": [],
            "confidence": 0.0
        }
    
    # Simple sentiment analysis (replace with actual NLP model)
    positive_keywords = [
        'tăng', 'tăng trưởng', 'khởi sắc', 'tích cực', 'thuận lợi', 'thành công',
        'lợi nhuận', 'đột phá', 'vượt trội', 'tối ưu', 'phát triển', 'mạnh mẽ',
        'increase', 'growth', 'positive', 'profit', 'success', 'strong'
    ]
    
    negative_keywords = [
        'giảm', 'sụt giảm', 'thất bại', 'khó khăn', 'rủi ro', 'thua lỗ',
        'đình trệ', 'yếu kém', 'tệ hại', 'khủng hoảng', 'bất ổn', 'lo ngại',
        'decrease', 'loss', 'risk', 'crisis', 'weak', 'concern'
    ]
    
    total_score = 0
    topics = set()
    
    for news in news_data:
        title = news.get('title', '').lower()
        content = news.get('content', '').lower()
        text = title + ' ' + content
        
        # Count positive and negative keywords
        positive_count = sum(1 for word in positive_keywords if word in text)
        negative_count = sum(1 for word in negative_keywords if word in text)
        
        # Calculate sentiment score for this article
        if positive_count > negative_count:
            article_score = min(positive_count / (positive_count + negative_count + 1), 1.0)
        elif negative_count > positive_count:
            article_score = -min(negative_count / (positive_count + negative_count + 1), 1.0)
        else:
            article_score = 0.0
        
        total_score += article_score
        
        # Extract topics (simple keyword matching)
        if 'lợi nhuận' in text or 'profit' in text:
            topics.add('lợi nhuận')
        if 'doanh thu' in text or 'revenue' in text:
            topics.add('doanh thu')
        if 'đầu tư' in text or 'investment' in text:
            topics.add('đầu tư')
        if 'm&a' in text or 'mua bán' in text:
            topics.add('m&a')
        if 'cổ tức' in text or 'dividend' in text:
            topics.add('cổ tức')
        if 'chia tách' in text or 'split' in text:
            topics.add('chia tách cổ phiếu')
        if 'phát hành' in text or 'issuance' in text:
            topics.add('phát hành')
    
    # Calculate average sentiment
    avg_score = total_score / len(news_data) if news_data else 0
    
    # Determine sentiment category
    if avg_score > 0.2:
        sentiment = "POSITIVE"
    elif avg_score < -0.2:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    
    return {
        "sentiment": sentiment,
        "score": round(avg_score, 3),
        "topics": list(topics),
        "confidence": min(abs(avg_score) + 0.5, 1.0),
        "article_count": len(news_data)
    }


def get_mock_news_data(ticker: str) -> List[Dict[str, Any]]:
    """
    Generate mock news data for Vietnam stocks
    """
    import random
    
    # Vietnam-specific news templates
    positive_templates = [
        f"{ticker} báo cáo lợi nhuận tăng trưởng ấn tượng trong quý 3",
        f"{ticker} công bố dự án đầu tư mới trị giá hàng nghìn tỷ đồng",
        f"{ticker} nhận được phê duyệt tăng vốn điều lệ",
        f"{ticker} chia cổ tức đột phá với tỷ lệ 30%",
        f"{ticker} ký kết hợp đồng chiến lược với đối tác nước ngoài",
        f"Chuyên gia đánh giá tiềm năng tăng trưởng của {ticker}",
        f"{ticker} dẫn đầu ngành về hiệu quả hoạt động",
        f"{ticker} vượt chỉ tiêu doanh thu 9 tháng đầu năm"
    ]
    
    negative_templates = [
        f"{ticker} sụt giảm lợi nhuận do chi phí tăng cao",
        f"{ticker} đối mặt với khó khăn từ thị trường bất ổn",
        f"{ticker} hoãn kế hoạch phát hành cổ phiếu",
        f"{ticker} bị rà soát về tuân thủ quy định",
        f"{ticker} giảm dự tiêu sản nghiệp năm nay",
        f"Nhà đầu tư lo ngại về triển vọng của {ticker}",
        f"{ticker} gặp thách thức từ cạnh tranh gay gắt",
        f"{ticker} ảnh hưởng tiêu cực từ chính sách vĩ mô"
    ]
    
    neutral_templates = [
        f"{ticker} tổ chức đại hội đồng cổ đông thường niên",
        f"{ticker} công bố lịch giao dịch cổ phiếu",
        f"{ticker} bổ nhiệm nhân sự cấp cao mới",
        f"{ticker} cập nhật thông tin giao dịch nội bộ",
        f"{ticker} công bố kết quả hoạt động quý",
        f"Phân tích kỹ thuật cổ phiếu {ticker}",
        f"{ticker} và triển vọng ngành trong 6 tháng cuối năm",
        f"Cập nhật thông tin từ {ticker}"
    ]
    
    news_sources = ["CafeF", "Vietstock", "NDH", "FPTS", "VNDirect", "SJC", "TCBS"]
    
    news_data = []
    num_news = random.randint(5, 15)
    
    for i in range(num_news):
        # Randomly choose sentiment
        rand = random.random()
        if rand < 0.4:
            template = random.choice(positive_templates)
        elif rand < 0.7:
            template = random.choice(neutral_templates)
        else:
            template = random.choice(negative_templates)
        
        # Generate random date within last 7 days
        days_ago = random.randint(0, 7)
        news_date = datetime.now() - timedelta(days=days_ago)
        
        news_data.append({
            "title": template,
            "content": f"Nội dung chi tiết về {template.lower()}...",
            "source": random.choice(news_sources),
            "published_date": news_date.isoformat(),
            "url": f"https://example.com/news/{ticker.lower()}-{i}"
        })
    
    return sorted(news_data, key=lambda x: x["published_date"], reverse=True)


def get_mock_news_sentiment(ticker: str) -> Dict[str, Any]:
    """
    Generate mock sentiment analysis for development
    """
    import random
    
    sentiment_score = random.uniform(-1, 1)
    
    if sentiment_score > 0.2:
        sentiment = "POSITIVE"
        topics = random.sample(['lợi nhuận', 'doanh thu', 'đầu tư', 'cổ tức'], random.randint(1, 3))
    elif sentiment_score < -0.2:
        sentiment = "NEGATIVE"
        topics = random.sample(['rủi ro', 'thua lỗ', 'khó khăn', 'sụt giảm'], random.randint(1, 3))
    else:
        sentiment = "NEUTRAL"
        topics = random.sample(['cổ tức', 'nhân sự', 'họp cổ đông', 'cập nhật'], random.randint(1, 2))
    
    mock_news = get_mock_news_data(ticker)
    
    return {
        "ticker": ticker,
        "sentiment": sentiment,
        "sentiment_score": round(sentiment_score, 3),
        "news_count": len(mock_news),
        "key_topics": topics,
        "recent_headlines": [item["title"] for item in mock_news[:5]],
        "analysis_timestamp": datetime.now().isoformat(),
        "news_sources": ["CafeF", "Vietstock", "NDH"],
        "detailed_analysis": {
            "sentiment": sentiment,
            "score": round(sentiment_score, 3),
            "topics": topics,
            "confidence": round(random.uniform(0.6, 0.9), 2),
            "article_count": len(mock_news)
        }
    }


def get_vietnam_market_sentiment() -> Dict[str, Any]:
    """
    Get overall Vietnam market sentiment
    """
    # This would integrate with market-wide sentiment indicators
    # For now, return mock data
    return {
        "market_sentiment": "NEUTRAL",
        "market_score": 0.1,
        "vn30_change": random.uniform(-2, 2),
        "hnx_change": random.uniform(-3, 3),
        "upcom_change": random.uniform(-4, 4),
        "market_volume": random.randint(5000, 15000),
        "market_topics": ["lãi suất", "lạm phát", "đầu tư công", "fii"],
        "analysis_timestamp": datetime.now().isoformat()
    }
