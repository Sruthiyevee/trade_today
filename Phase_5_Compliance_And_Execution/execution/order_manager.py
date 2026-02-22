import logging
from compliance.algo_id_gen import generate_algo_id
from compliance.audit_logger import log_execution

logger = logging.getLogger("advisory_logger")

def log_advisory_signal(ticker: str, consensus_decision: str, risk_flag: dict) -> dict:
    """
    The final step in this advisory-only architecture.
    Receives the approved logic from the Risk Manager
    and writes the final signal to the local DB for the user to review.
    """
    logger.info(f"Logging pure advisory signal for {ticker}: {consensus_decision}")
    
    # 1. Generate SEBI signature
    algo_id = generate_algo_id(ticker, consensus_decision)
    
    # 2. Check risk
    is_approved = risk_flag.get("risk_approved", False)
    
    if not is_approved:
        logger.warning(f"Order Blocked by Risk Layer: {risk_flag.get('rejection_reason')}")
        log_execution(algo_id, ticker, consensus_decision, False, risk_flag.get("rejection_reason", "Unknown"))
        return {"status": "blocked", "algo_id": algo_id, "reason": risk_flag.get('rejection_reason')}
        
    # 3. Advisory Only Logging
    try:
        # 4. Log successful advisory signal
        log_execution(algo_id, ticker, consensus_decision, True, "Approved")
        
        return {
            "status": "advisory_logged",
            "algo_id": algo_id,
            "advisory_signal": consensus_decision
        }
    except Exception as e:
        logger.error(f"Logging failed: {str(e)}")
        log_execution(algo_id, ticker, consensus_decision, False, f"Database Error: {str(e)}")
        return {"status": "failed", "algo_id": algo_id, "reason": str(e)}
