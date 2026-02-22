import os
import sys
import sqlite3

# Ensure the root of Phase 5 is in the python path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root, "Phase_5_Compliance_And_Execution"))

from compliance.algo_id_gen import generate_algo_id
from execution.order_manager import log_advisory_signal
from compliance.audit_logger import DB_PATH

def run_tests():
    print("\n--- Testing Phase 5: SEBI Compliance & Execution ---")
    
    # 1. Test Algo ID Generation
    print("\n[1] Testing Algorithmic SEBI ID Signature Generation:")
    algo_sig = generate_algo_id("RELIANCE.NS", "BUY")
    assert algo_sig.startswith("AI_"), "Signature must use the 'AI_' algorithmic prefix."
    assert len(algo_sig) == 15, "Signature string length should be normalized to 15 chars."
    print(f"-> Generated Valid Hash: {algo_sig}")
    
    # 2. Test Rejected Order Routing & Audit 
    print("\n[2] Testing Execution Block (Risk Rejected):")
    blocked_route = log_advisory_signal("TCS.NS", "BUY", {"risk_approved": False, "rejection_reason": "Low Confidence"})
    assert blocked_route["status"] == "blocked", "Order must not route if risk is unapproved."
    print(f"-> Safely Blocked! Algo ID tracking number: {blocked_route['algo_id']}")
    
    # 3. Test Approved Order Routing & Audit
    print("\n[3] Testing Execution Approved (Simulated Advisory Hook):")
    approved_route = log_advisory_signal("INFY.NS", "SELL", {"risk_approved": True, "rejection_reason": "Approved"})
    assert approved_route["status"] == "advisory_logged", "Route ought to be logged if risk passes."
    print(f"-> Trade Triggered! SEBI Audit ID: {approved_route['algo_id']} | Signal: {approved_route['advisory_signal']}")

    # 4. Verify SQLite Write Results
    print("\n[4] Verifying SQLite 100% Free Persistent Storage:")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT algo_id, ticker, action, executed FROM executions")
    rows = cursor.fetchall()
    conn.close()
    
    assert len(rows) >= 2, "Database must hold at least the 2 previous test writes."
    print(f"-> Dump from Phase 5 Database: \n{rows[-2:]}")
    
    print("\n-> All Phase 5 simulated tests passed successfully.\n")

if __name__ == "__main__":
    run_tests()
