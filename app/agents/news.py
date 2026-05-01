from app.agents.base import BaseAgent
from app.services.llm import LLMRouter
from app.services.news_sentiment import analyze_vietnam_stock_news


class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__("c:/Users/nguye/Downloads/Stock_Analyzer/app/prompts/news.txt", LLMRouter())
    
    def __call__(self, state):
        news_data = analyze_vietnam_stock_news(state["ticker"])
        
        summary = self.run_llm({
            "ticker": state["ticker"],
            "company_name": state["market_data"].get("company_name", ""),
            "sentiment": news_data["sentiment"],
            "sentiment_score": news_data["sentiment_score"],
            "news_count": news_data["news_count"],
            "key_topics": ", ".join(news_data["key_topics"]),
            "recent_headlines": "\n".join(news_data["recent_headlines"][:3])
        })

        state["news_data"] = {
            **news_data,
            "summary": summary
        }
        return state