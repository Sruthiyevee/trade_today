import os
import logging

logger = logging.getLogger("debate_nodes")

def run_bull_researcher(ticker: str, agent_insights: list) -> dict:
    """
    Takes the initial insights from TAA, FAA, and SAA, and forcefully 
    looks for the bullish permutation or upside risk.
    """
    logger.info(f"Bull Agent analyzing insights for {ticker}...")
    # Mocking standard ChatGroq LLM response
    return {
        "agent_name": "Bull Researcher",
        "stance": "Bullish",
        "reasoning": "Mock: Technicals show strong momentum ignoring fundamental debt.",
        "confidence_score": 0.90
    }

def run_bear_researcher(ticker: str, agent_insights: list) -> dict:
    """
    Acts as the devil's advocate to the Bull Researcher, finding flaws
    in the current pipeline insights.
    """
    logger.info(f"Bear Agent analyzing insights for {ticker}...")
    # Mocking standard ChatGroq LLM response
    return {
        "agent_name": "Bear Researcher",
        "stance": "Bearish",
        "reasoning": "Mock: The sentiment is artificially inflated by recent unconfirmed news.",
        "confidence_score": 0.70
    }
