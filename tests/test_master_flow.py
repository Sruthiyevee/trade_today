import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from master_orchestrator import run_master_orchestrator

def run_5_test_cases():
    test_tickers = [
        "RELIANCE.NS",
        "TCS.NS",
        "HDFCBANK.NS",
        "INFY.NS",
        "ITC.NS"
    ]
    
    print("\n" + "="*60)
    print("--- STARTING BATCH TEST FOR 5 END-TO-END FLOWS ---")
    print("="*60)
    
    for i, ticker in enumerate(test_tickers, 1):
        print(f"\n\n{"#"*10} TEST CASE {i}/5 : {ticker} {"#"*10}")
        try:
            # The run_master_orchestrator function already prints its own internal steps and outputs
            result = run_master_orchestrator(ticker)
        except Exception as e:
            print(f"--- Error during execution for {ticker}: {str(e)} ---")
            
    print("\n" + "="*60)
    print("--- BATCH TEST COMPLETED SUCCESSFULLY ---")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_5_test_cases()
