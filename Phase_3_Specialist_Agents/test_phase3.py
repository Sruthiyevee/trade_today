import os
import sys

# Ensure the root of Phase 3 is in the python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agents.technical.ta_agent import run_technical_analysis
from agents.fundamental.fa_agent import run_fundamental_analysis
from agents.debate.adversarial_agents import run_bull_researcher, run_bear_researcher

def run_tests():
    print("\n--- Testing Phase 3: Specialist Agents ---")
    
    # 1. Test Technical Analyst (TAA)
    print("\n[1] Testing Technical Analyst (Groq/Llama3 Mock):")
    ta_result = run_technical_analysis("RELIANCE.NS", {"close": 2500, "sma_50": 2450})
    assert ta_result.get("agent_name") == "Technical Analyst", "Agent name mismatch"
    print(f"-> TAA Stance: {ta_result.get('stance')} | Score: {ta_result.get('confidence_score')}")
    
    # 2. Test Fundamental Analyst (FAA)
    print("\n[2] Testing Fundamental Analyst (Gemini Flash Mock):")
    fa_result = run_fundamental_analysis("RELIANCE.NS", "Revenue grew by 15%.")
    assert fa_result.get("agent_name") == "Fundamental Analyst", "Agent name mismatch"
    print(f"-> FAA Stance: {fa_result.get('stance')} | Score: {fa_result.get('confidence_score')}")
    
    # 3. Test Adversarial Synthesis (Bull & Bear)
    print("\n[3] Testing Adversarial Nodes (Llama3 Mock):")
    bull_res = run_bull_researcher("RELIANCE.NS", [ta_result, fa_result])
    bear_res = run_bear_researcher("RELIANCE.NS", [ta_result, fa_result])
    assert bull_res.get("stance") == "Bullish", "Bull node should return Bullish"
    assert bear_res.get("stance") == "Bearish", "Bear node should return Bearish"
    print(f"-> Bull: {bull_res.get('reasoning')}")
    print(f"-> Bear: {bear_res.get('reasoning')}")
    
    print("\n-> All Phase 3 simulated tests passed successfully.\n")

if __name__ == "__main__":
    run_tests()
