from app.agents.base import BaseAgent
from app.services.llm import LLMRouter


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/planner.txt", LLMRouter())
    
    def __call__(self, state):
        state["tasks"] = [
            "market_analysis",
            "technical_analysis",
            "news_analysis",
            "risk_analysis",
            "decision"
        ]
        
        # Generate analysis plan
        summary = self.run_llm({
            "ticker": state["ticker"],
            "tasks": ", ".join(state["tasks"])
        })
        
        state["plan"] = {
            "tasks": state["tasks"],
            "summary": summary
        }
        return state