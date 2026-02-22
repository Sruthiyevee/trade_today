from typing import TypedDict, Annotated, List, Dict, Any
import operator
from pydantic import BaseModel, Field

class MarketData(BaseModel):
    """Normalized schema for ticker data flowing into the graph."""
    ticker: str
    current_price: float = 0.0
    technical_indicators: Dict[str, Any] = Field(default_factory=dict)
    fundamental_metrics: Dict[str, Any] = Field(default_factory=dict)
    sentiment_score: float = 0.0

class AgentReasoning(BaseModel):
    """Standardized output structure for agent debates."""
    agent_name: str
    stance: str # e.g., "Bullish", "Bearish", "Neutral"
    reasoning: str
    confidence_score: float

class AnalystState(TypedDict):
    """
    The shared memory core (LangGraph State) for the Portfolio Manager workflow. 
    `messages` might be added later if utilizing pure conversational chains.
    """
    # Inputs
    user_query: str
    active_ticker: str
    
    # Aggregated Insights (Using operator.add to append items if operating concurrently)
    market_data: MarketData
    agent_debates: Annotated[List[AgentReasoning], operator.add]
    
    # Portfolio Manager Outputs
    final_decision: str       # "BUY", "SELL", "HOLD"
    execution_plan: str       # Notes for the Risk Manager / Execution step
    
    # Routing constraints
    risk_approved: bool 
    error_logs: Annotated[List[str], operator.add]
