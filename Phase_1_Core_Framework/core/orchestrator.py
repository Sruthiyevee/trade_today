from langgraph.graph import StateGraph, END
from typing import Dict, Any
from core.state import AnalystState, MarketData, AgentReasoning

def mock_market_data_node(state: AnalystState):
    """Dummy node representing initial data ingestion."""
    print(f"[Orchestrator] Ingesting data for {state['active_ticker']}...")
    return {
        "market_data": MarketData(
            ticker=state["active_ticker"],
            current_price=100.0,
            sentiment_score=0.5
        )
    }

def mock_portfolio_manager_node(state: AnalystState):
    """Dummy node representing the final decision consensus."""
    print("[Orchestrator] Generating final portfolio decision...")
    return {
        "final_decision": "HOLD",
        "execution_plan": "Awaiting full agent integrations before trading.",
        "risk_approved": True
    }

# Build the simplified graph
builder = StateGraph(AnalystState)

# Add Nodes
builder.add_node("ingest_data", mock_market_data_node)
builder.add_node("portfolio_manager", mock_portfolio_manager_node)

# Set edges
builder.set_entry_point("ingest_data")
builder.add_edge("ingest_data", "portfolio_manager")
builder.add_edge("portfolio_manager", END)

# Compile Graph
graph = builder.compile()

# Example runner for local testing
def run_analyst(ticker: str, query: str = "Analyze this stock"):
    initial_state = AnalystState(
        user_query=query,
        active_ticker=ticker,
        market_data=MarketData(ticker=ticker),
        agent_debates=[],
        final_decision="",
        execution_plan="",
        risk_approved=False,
        error_logs=[]
    )
    
    events = graph.invoke(initial_state)
    return events
