import logging
from typing import List, Dict

logger = logging.getLogger("risk_manager")

def evaluate_portfolio_risk(ticker: str, consensus_decision: str, agent_insights: List[Dict]) -> dict:
    """
    The final safety check before generating an execution instruction.
    Calculates if the agent confidence levels surpass the minimum threshold.
    """
    logger.info(f"Evaluating Risk limit for {ticker} | Consensus: {consensus_decision}")
    
    # If consensus isn't definitive, block the trade.
    if consensus_decision.upper() not in ["BUY", "SELL"]:
        return {
            "risk_approved": False,
            "rejection_reason": "Consensus is merely HOLD or UNKNOWN."
        }
        
    # Example logic: Average confidence of all participating agents must be > 0.70
    if not agent_insights:
        return {"risk_approved": False, "rejection_reason": "No agent insights provided to Risk Manager."}
        
    total_confidence = sum([insight.get("confidence_score", 0.0) for insight in agent_insights])
    avg_confidence = total_confidence / len(agent_insights)
    
    logger.info(f"Average Agent Confidence: {avg_confidence:.2f}")
    
    if avg_confidence < 0.70:
        return {
            "risk_approved": False,
            "rejection_reason": f"Agent certainty ({avg_confidence:.2f}) is below the 0.70 safety threshold."
        }
        
    return {
        "risk_approved": True,
        "rejection_reason": "Approved"
    }
