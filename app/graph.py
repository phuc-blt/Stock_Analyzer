from langgraph.graph import StateGraph, END
from app.state import StockAnalysisState
from app.agents.planner import PlannerAgent
from app.agents.market import MarketAgent
from app.agents.technical import TechnicalAgent
from app.agents.news import NewsAgent
from app.agents.risk import RiskAgent
from app.agents.decision import DecisionAgent


def build_graph():
    # Initialize agents (they handle their own LLM initialization)
    planner = PlannerAgent()
    market = MarketAgent()
    technical = TechnicalAgent()
    news = NewsAgent()
    risk = RiskAgent()
    decision = DecisionAgent()

    # Create the state graph
    graph = StateGraph(StockAnalysisState)

    # Add nodes
    graph.add_node("planner", planner)
    graph.add_node("market", market)
    graph.add_node("technical", technical)
    graph.add_node("news", news)
    graph.add_node("risk", risk)
    graph.add_node("decision", decision)

    # Define the workflow
    graph.set_entry_point("planner")
    graph.add_edge("planner", "market")
    graph.add_edge("market", "technical")
    graph.add_edge("technical", "news")
    graph.add_edge("news", "risk")
    graph.add_edge("risk", "decision")
    graph.add_edge("decision", END)

    return graph.compile()