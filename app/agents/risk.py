from app.agents.base import BaseAgent
from app.services.llm import LLMRouter


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("c:/Users/nguye/Downloads/Stock_Analyzer/app/prompts/risk.txt", LLMRouter())
    
    def __call__(self, state):
        market_data = state["market_data"]
        technical_data = state["technical_data"]
        
        # Vietnam market specific risk factors
        beta = market_data.get("beta", 1)
        volatility = technical_data.get("volatility", 0.2)
        volume_ratio = market_data.get("volume", 0) / market_data.get("avg_volume", 1)
        pe_ratio = market_data.get("pe_ratio", 15)
        
        # Calculate risk score (0-100)
        risk_score = 0
        
        # Beta risk (30% weight)
        if beta < 0.8:
            risk_score += 10
        elif beta < 1.2:
            risk_score += 25
        elif beta < 1.8:
            risk_score += 50
        else:
            risk_score += 75
            
        # Volatility risk (25% weight)
        if volatility < 0.15:
            risk_score += 10
        elif volatility < 0.25:
            risk_score += 25
        elif volatility < 0.35:
            risk_score += 50
        else:
            risk_score += 75
            
        # Volume risk (20% weight)
        if volume_ratio > 1.5:
            risk_score += 15
        elif volume_ratio < 0.5:
            risk_score += 40
        else:
            risk_score += 20
            
        # Valuation risk (25% weight)
        if pe_ratio < 10:
            risk_score += 15
        elif pe_ratio < 20:
            risk_score += 20
        elif pe_ratio < 30:
            risk_score += 40
        else:
            risk_score += 60
        
        # Determine risk level
        if risk_score < 30:
            risk = "LOW"
        elif risk_score < 60:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        summary = self.run_llm({
            "ticker": state["ticker"],
            "company_name": market_data.get("company_name", ""),
            "beta": beta,
            "volatility": volatility,
            "volume_ratio": volume_ratio,
            "pe_ratio": pe_ratio,
            "risk_score": risk_score,
            "risk": risk,
            "exchange": market_data.get("exchange", "HOSE")
        })

        state["risk_data"] = {
            "beta": beta,
            "volatility": volatility,
            "volume_ratio": volume_ratio,
            "pe_ratio": pe_ratio,
            "risk_score": risk_score,
            "risk": risk,
            "summary": summary
        }
        return state