from app.agents.base import BaseAgent
from app.services.llm import LLMRouter


class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/decision.txt", LLMRouter())
    
    def __call__(self, state):
        market_data = state["market_data"]
        technical_data = state["technical_data"]
        news_data = state["news_data"]
        risk_data = state["risk_data"]
        
        # Extract key signals
        tech_signal = technical_data["signal"]
        tech_confidence = technical_data.get("confidence", 50)
        sentiment = news_data["sentiment"]
        sentiment_score = news_data.get("sentiment_score", 0)
        risk_level = risk_data["risk"]
        risk_score = risk_data["risk_score"]
        
        # Enhanced decision logic for Vietnam market
        recommendation = "HOLD"
        confidence = 50
        reasoning = []
        
        # Technical analysis weight (40%)
        if tech_signal == "BUY":
            if risk_level != "HIGH":
                recommendation = "BUY"
                confidence = min(confidence + 30, 90)
                reasoning.append(f"Technical signal: {tech_signal} (confidence: {tech_confidence}%)")
            else:
                reasoning.append("Technical BUY signal overridden by HIGH risk")
        elif tech_signal == "SELL":
            recommendation = "SELL"
            confidence = min(confidence + 35, 90)
            reasoning.append(f"Technical signal: {tech_signal} (confidence: {tech_confidence}%)")
        
        # News sentiment weight (25%)
        if sentiment == "POSITIVE" and sentiment_score > 0.6:
            if recommendation == "HOLD":
                recommendation = "BUY"
                confidence = min(confidence + 20, 85)
            elif recommendation == "BUY":
                confidence = min(confidence + 15, 90)
            reasoning.append(f"Positive news sentiment: {sentiment_score:.2f}")
        elif sentiment == "NEGATIVE" and sentiment_score < -0.6:
            if recommendation == "HOLD":
                recommendation = "SELL"
                confidence = min(confidence + 25, 85)
            elif recommendation == "BUY":
                recommendation = "HOLD"
                confidence = max(confidence - 20, 30)
            reasoning.append(f"Negative news sentiment: {sentiment_score:.2f}")
        
        # Risk assessment weight (20%)
        if risk_level == "HIGH":
            if recommendation == "BUY":
                recommendation = "HOLD"
                confidence = max(confidence - 25, 30)
            reasoning.append(f"High risk level: {risk_score}/100")
        elif risk_level == "LOW" and recommendation == "HOLD":
            confidence = min(confidence + 10, 70)
            reasoning.append(f"Low risk level: {risk_score}/100")
        
        # Market conditions weight (15%)
        pe_ratio = market_data.get("pe_ratio", 15)
        if pe_ratio < 12 and recommendation != "SELL":
            confidence = min(confidence + 5, 85)
            reasoning.append(f"Attractive valuation: P/E {pe_ratio}")
        elif pe_ratio > 35 and recommendation != "BUY":
            confidence = min(confidence + 5, 85)
            reasoning.append(f"High valuation: P/E {pe_ratio}")

        summary = self.run_llm({
            "ticker": state["ticker"],
            "company_name": market_data.get("company_name", ""),
            "technical_signal": tech_signal,
            "technical_confidence": tech_confidence,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": "; ".join(reasoning),
            "pe_ratio": pe_ratio,
            "exchange": market_data.get("exchange", "HOSE")
        })

        state["final_decision"] = {
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": reasoning,
            "summary": summary,
            "analysis_timestamp": state.get("timestamp", "")
        }
        return state