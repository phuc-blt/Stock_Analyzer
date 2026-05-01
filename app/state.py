from typing import TypedDict, Dict, Any, List, Optional

class StockAnalysisState(TypedDict):
    # Basic inputs
    ticker: str
    horizon: str
    risk_tolerance: Optional[str]
    timestamp: str
    
    # Planning phase
    tasks: List[str]
    plan: Dict[str, Any]
    
    # Analysis phases
    market_data: Dict[str, Any]
    technical_data: Dict[str, Any]
    news_data: Dict[str, Any]
    risk_data: Dict[str, Any]
    
    # Final decision
    final_decision: Dict[str, Any]
    
    # Optional additional context
    metadata: Optional[Dict[str, Any]]