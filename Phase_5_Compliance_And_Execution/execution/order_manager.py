import logging
from compliance.algo_id_gen import generate_algo_id
from compliance.audit_logger import log_execution

# In a real run, this would import from the actual root
# from Phase_2_Data_Connectivity.data_connectors.broker_api import FreeBrokerConnector

logger = logging.getLogger("order_manager")

def route_order(ticker: str, consensus_decision: str, risk_flag: dict) -> dict:
    """
    The final bridge. Receives the approved logic from the Risk Manager
    and triggers the free broker API hooks while writing to the local DB.
    """
    logger.info(f"Routing order for {ticker}: {consensus_decision}")
    
    # 1. Generate SEBI signature
    algo_id = generate_algo_id(ticker, consensus_decision)
    
    # 2. Check risk
    is_approved = risk_flag.get("risk_approved", False)
    
    if not is_approved:
        logger.warning(f"Order Blocked by Risk Layer: {risk_flag.get('rejection_reason')}")
        log_execution(algo_id, ticker, consensus_decision, False, risk_flag.get("rejection_reason", "Unknown"))
        return {"status": "blocked", "algo_id": algo_id, "reason": risk_flag.get('rejection_reason')}
        
    # 3. Simulate Broker Execution (Using the logic from Phase 2)
    try:
        # Mocking the connector execution
        # connector = FreeBrokerConnector()
        # broker_res = connector.execute_limit_order(...)
        broker_res = {"status": "success", "order_id": "MOCK_BROKER_999"}
        
        # 4. Log successful execution
        log_execution(algo_id, ticker, consensus_decision, True, "Approved")
        
        return {
            "status": "executed",
            "algo_id": algo_id,
            "broker_res": broker_res
        }
    except Exception as e:
        logger.error(f"Broker connection failed: {str(e)}")
        log_execution(algo_id, ticker, consensus_decision, False, f"Broker Error: {str(e)}")
        return {"status": "failed", "algo_id": algo_id, "reason": str(e)}
