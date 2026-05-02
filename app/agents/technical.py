from app.agents.base import BaseAgent
from app.services.llm import LLMRouter
from app.services.indicators import calculate_vietnam_indicators


class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/technical.txt", LLMRouter())
    
    def __call__(self, state):
        indicators = calculate_vietnam_indicators(state["market_data"]["history"])
        
        # Enhanced signal logic for Vietnam market
        signal = "HOLD"
        confidence = 50
        
        if indicators["rsi"] < 30 and indicators["macd"] > 0 and indicators["ma20"] > indicators["ma50"]:
            signal = "BUY"
            confidence = 80
        elif indicators["rsi"] < 35 and indicators["macd"] > 0:
            signal = "BUY"
            confidence = 65
        elif indicators["rsi"] > 75:
            signal = "SELL"
            confidence = 75
        elif indicators["rsi"] > 70 and indicators["macd"] < 0:
            signal = "SELL"
            confidence = 60

        summary = self.run_llm({
            "ticker": state["ticker"],
            "company_name": state["market_data"].get("company_name", ""),
            "current_price": state["market_data"]["price"],
            "rsi": indicators["rsi"],
            "macd": indicators["macd"],
            "signal_line": indicators["signal_line"],
            "ma20": indicators["ma20"],
            "ma50": indicators["ma50"],
            "bollinger_upper": indicators["bollinger_upper"],
            "bollinger_lower": indicators["bollinger_lower"],
            "volume_sma": indicators["volume_sma"],
            "signal": signal,
            "confidence": confidence
        })

        state["technical_data"] = {
            **indicators,
            "signal": signal,
            "confidence": confidence,
            "summary": summary
        }
        return state