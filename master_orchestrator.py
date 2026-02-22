import os
import sys
import logging

# 1. PATH RESOLUTION: Inject all Phase directories into sys.path
# This is the critical fix for the fragmented architecture.
root_dir = os.path.dirname(os.path.abspath(__file__))
phases = [
    "Phase_1_Core_Framework",
    "Phase_2_Data_Connectivity",
    "Phase_3_Specialist_Agents",
    "Phase_4_Risk_And_Observability",
    "Phase_5_Compliance_And_Execution"
]
for phase in phases:
    sys.path.insert(0, os.path.join(root_dir, phase))

# Now we can safely import across modules!
from langgraph.graph import StateGraph, END
from core.state import AnalystState, MarketData

# Import actual logic from other phases
from agents.technical.ta_agent import run_technical_analysis
from agents.fundamental.fa_agent import run_fundamental_analysis
from agents.sentiment.sentiment_agent import run_sentiment_analysis
from core.risk_manager import evaluate_portfolio_risk
from execution.order_manager import log_advisory_signal
from data_connectors.yfinance_data import fetch_live_ohlcv

logger = logging.getLogger("master_orchestrator")

def master_ingest_node(state: AnalystState):
    """(Phase 2 integration)"""
    ticker = state["active_ticker"]
    print(f"[Master] Gathering remote OHLCV (yfinance) and Fundamentals for {ticker}...")
    
    ohlcv_data = fetch_live_ohlcv(ticker)
    
    current_px = ohlcv_data.get("current_price", 0.0)
    
    return {
        "market_data": MarketData(ticker=ticker, current_price=current_px, technical_indicators=ohlcv_data)
    }

def master_specialist_node(state: AnalystState):
    """(Phase 3 integration) Calls actual agents."""
    print("[Master] Triggering Technical, Fundamental, and Sentiment Agents...")
    ticker = state["active_ticker"]
    
    # Run the real agents (these will fallback to mock data if API keys aren't set)
    ta_res = run_technical_analysis(ticker, {"mock": "ohlcv"})
    fa_res = run_fundamental_analysis(ticker, {"mock": "rag_docs"})
    sa_res = run_sentiment_analysis(ticker, {"mock": "news_articles"})
    
    return {
        "agent_debates": [ta_res, fa_res, sa_res]
    }

def master_risk_node(state: AnalystState):
    """(Phase 4 integration)"""
    print("[Master] Evaluating Portfolio Risk based on Agent Consensus...")
    risk_assessment = evaluate_portfolio_risk(state["active_ticker"], "BUY", state["agent_debates"])
    
    return {
        "final_decision": "BUY", # Simplified consensus
        "risk_approved": risk_assessment["risk_approved"],
        "execution_plan": risk_assessment.get("rejection_reason", "Approved")
    }

def master_advisory_node(state: AnalystState):
    """(Phase 5 integration - Advisory Only)"""
    if state["risk_approved"]:
        print("[Master] Risk passed. Logging final advisory signal to SQLite...")
    else:
        print("[Master] Risk failed. Logging blocked advisory signal...")
        
    route_res = log_advisory_signal(
        state["active_ticker"], 
        state["final_decision"], 
        {"risk_approved": state["risk_approved"], "rejection_reason": state["execution_plan"]}
    )
    return {"error_logs": [f"Advisory status: {route_res['status']}"]}

# Build the UNIFIED Graph
builder = StateGraph(AnalystState)

builder.add_node("ingest", master_ingest_node)
builder.add_node("specialists", master_specialist_node)
builder.add_node("risk_layer", master_risk_node)
builder.add_node("advisory_logger", master_advisory_node)

builder.set_entry_point("ingest")
builder.add_edge("ingest", "specialists")
builder.add_edge("specialists", "risk_layer")
builder.add_edge("risk_layer", "advisory_logger")
builder.add_edge("advisory_logger", END)

master_app = builder.compile()

def run_master_orchestrator(ticker: str):
    """Trigger the fully integrated graph end-to-end."""
    print("\n" + "="*50)
    print(f"--- INITIALIZING MASTER INTEGRATION RUN: {ticker} ---")
    print("="*50)
    
    initial_state = AnalystState(
        user_query="Analyze", active_ticker=ticker, market_data=MarketData(ticker=ticker),
        agent_debates=[], final_decision="", execution_plan="", risk_approved=False, error_logs=[]
    )
    
    result = master_app.invoke(initial_state)
    print("\n--- FINAL MASTER STATE ---")
    print(f"Risk Approved: {result['risk_approved']}")
    print(f"Execution Log: {result['error_logs']}")
    return result

if __name__ == "__main__":
    run_master_orchestrator("RELIANCE.NS")
