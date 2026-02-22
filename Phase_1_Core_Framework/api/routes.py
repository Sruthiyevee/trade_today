from fastapi import APIRouter
from core.orchestrator import run_analyst
import logging

router = APIRouter(prefix="/analyze", tags=["Trading Graph"])
logger = logging.getLogger("api")

@router.post("/")
async def start_analysis(ticker: str, query: str):
    """
    Triggers the LangGraph orchestration loop for the specified stock.
    In Phase 1, everything is returned directly without streaming.
    """
    logger.info(f"Triggered analysis for ticker: {ticker}")
    
    # 1. Start the Graph Run
    try:
        final_state = run_analyst(ticker, query)
        
        # 2. Extract Key Outcomes
        response = {
            "status": "success",
            "ticker": ticker,
            "final_decision": final_state.get("final_decision", "UNKNOWN"),
            "risk_approved": final_state.get("risk_approved", False),
            "execution_plan": final_state.get("execution_plan", ""),
        }
        return response
    
    except Exception as e:
        logger.error(f"Graph execution failed: {str(e)}")
        return {"status": "error", "message": str(e)}
