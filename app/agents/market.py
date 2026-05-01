from app.agents.base import BaseAgent
from app.services.llm import LLMRouter
from app.services.market_data import fetch_vietnam_stock_data


class MarketAgent(BaseAgent):
    def __init__(self):
        super().__init__("c:/Users/nguye/Downloads/Stock_Analyzer/app/prompts/market.txt", LLMRouter())
    
    def __call__(self, state):
        data = fetch_vietnam_stock_data(state["ticker"])
        
        summary = self.run_llm({
            "ticker": state["ticker"],
            "company_name": data.get("company_name", ""),
            "price": data["price"],
            "pe_ratio": data["pe_ratio"],
            "pb_ratio": data.get("pb_ratio", "N/A"),
            "market_cap": data["market_cap"],
            "volume": data.get("volume", 0),
            "exchange": data.get("exchange", "HOSE"),
            "industry": data.get("industry", ""),
            "dividend_yield": data.get("dividend_yield", 0)
        })

        state["market_data"] = {
            **data,
            "summary": summary
        }
        return state