import os
import sys

# Ensure the root of Phase 4 is in the python path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root, "Phase_4_Risk_And_Observability"))

from core.risk_manager import evaluate_portfolio_risk
from core.langfuse_config import get_langfuse_handler

def run_tests():
    print("\n--- Testing Phase 4: Risk & Observability ---")
    
    # 1. Test Langfuse Callback Logic
    print("\n[1] Testing Langfuse Telemetry Loader:")
    # First with no env vars
    os.environ['LANGFUSE_PUBLIC_KEY'] = 'dummy_pk'
    handler_none = get_langfuse_handler()
    assert handler_none is None, "Handler should return None when missing keys."
    print("-> Successfully bypassed Langfuse when keys are absent.")
    
    # 2. Test Risk Manager (Approval Path)
    print("\n[2] Testing Risk Manager (Approval Path):")
    mock_strong_agents = [
        {"agent_name": "TAA", "confidence_score": 0.85},
        {"agent_name": "FAA", "confidence_score": 0.80},
    ]
    approved_res = evaluate_portfolio_risk("RELIANCE.NS", "BUY", mock_strong_agents)
    assert approved_res["risk_approved"], "High confidence consensus should be approved."
    print(f"-> Approval Status: {approved_res['rejection_reason']}")
    
    # 3. Test Risk Manager (Rejection Path - Low Confidence)
    print("\n[3] Testing Risk Manager (Rejection Path - Low Confidence):")
    mock_weak_agents = [
        {"agent_name": "Bull", "confidence_score": 0.50},
        {"agent_name": "Bear", "confidence_score": 0.60},
    ]
    rejected_res = evaluate_portfolio_risk("TCS.NS", "SELL", mock_weak_agents)
    assert not rejected_res["risk_approved"], "Low confidence consensus should be rejected."
    print(f"-> Rejection Status: {rejected_res['rejection_reason']}")

    # 4. Test Risk Manager (Rejection Path - Indecisive)
    print("\n[4] Testing Risk Manager (Rejection Path - Indecisive Consensus):")
    mock_hold_agents = [
        {"agent_name": "TAA", "confidence_score": 0.90},
    ]
    indecisive_res = evaluate_portfolio_risk("INFY.NS", "HOLD", mock_hold_agents)
    assert not indecisive_res["risk_approved"], "HOLD consensus should block automated execution."
    print(f"-> Rejection Status: {indecisive_res['rejection_reason']}")
    
    print("\n-> All Phase 4 simulated tests passed successfully.\n")

if __name__ == "__main__":
    run_tests()
