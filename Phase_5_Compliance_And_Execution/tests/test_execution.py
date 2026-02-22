import os
import sys
import sqlite3

# Ensure the root of Phase 5 is in the python path
phase5_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, phase5_root)

from compliance.algo_id_gen import generate_algo_id
from execution.order_manager import route_order
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
    blocked_route = route_order("TCS.NS", "BUY", {"risk_approved": False, "rejection_reason": "Low Confidence"})
    assert blocked_route["status"] == "blocked", "Order must not route if risk is unapproved."
    print(f"-> Safely Blocked! Algo ID tracking number: {blocked_route['algo_id']}")
    
    # 3. Test Approved Order Routing & Audit
    print("\n[3] Testing Execution Approved (Simulated API Hook):")
    approved_route = route_order("INFY.NS", "SELL", {"risk_approved": True, "rejection_reason": "Approved"})
    assert approved_route["status"] == "executed", "Route ought to be executed if risk passes."
    print(f"-> Trade Triggered! SEBI Audit ID: {approved_route['algo_id']} | Broker ID: {approved_route['broker_res']['order_id']}")

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
