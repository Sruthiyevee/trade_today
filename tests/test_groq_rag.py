import os
import sys

# Load API key from environment (set in .streamlit/secrets.toml or shell)
os.environ.setdefault('GROQ_API_KEY', os.environ.get('GROQ_API_KEY', ''))

root = r'd:\Product Management\cursor\trade_today'
sys.path.insert(0, root)
sys.path.insert(0, root + r'\Phase_3_Specialist_Agents')
sys.path.insert(0, root + r'\Phase_2_Data_Connectivity')

import logging
logging.basicConfig(level=logging.WARNING)

from agents.fundamental.fa_agent import run_fundamental_analysis

result = run_fundamental_analysis('RELIANCE.NS')
print()
print('=== FUNDAMENTAL AGENT OUTPUT (Groq RAG) ===')
print('Agent:', result.get('agent_name'))
print('Stance:', result.get('stance'))
print('Confidence:', result.get('confidence_score'))
print('Reasoning:', result.get('reasoning'))
