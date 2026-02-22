import os
import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
# Using relative imports assuming this will eventually be wrapped by the orchestrator 
# from core.state import AgentReasoning

logger = logging.getLogger("ta_agent")

def run_technical_analysis(ticker: str, ohlcv_dummy_data: dict) -> dict:
    """
    Simulates the Technical Analyst Agent (TAA).
    In production, this node receives OHLCV data and utilizes a fast Groq-hosted
    Llama 3 model (8B or 70B) to reason about moving averages, RSI, and MACD.
    """
    logger.info(f"Running TAA on {ticker} using Groq Llama 3...")
    
    api_key = os.getenv("GROQ_API_KEY", "dummy_key")
    if api_key == "dummy_key":
        logger.warning("No GROQ_API_KEY found, returning mock technical analysis.")
        return {
            "agent_name": "Technical Analyst",
            "stance": "Bullish",
            "reasoning": "API Call Failed (Missing Key) - Fallback Mock: 50 SMA crossed above 200 SMA indicating Golden Cross.",
            "confidence_score": 0.85
        }
        
    # Example LangChain setup for when the API key is provided
    try:
        llm = ChatGroq(temperature=0.1, model_name="llama-3.1-8b-instant")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Technical Analyst focusing on the Indian market. Analyze the given indicators and output a purely technical stance (Bullish/Bearish/Neutral)."),
            ("human", "Assess {ticker} based on this data: {data}")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"ticker": ticker, "data": ohlcv_dummy_data})
        
        return {
            "agent_name": "Technical Analyst",
            "stance": "Derived via LLM",
            "reasoning": str(response.content),
            "confidence_score": 0.75 # Typically derived from logprobs or a structured output parser
        }
        
    except Exception as e:
        logger.error(f"TAA failed: {str(e)}")
        return {
            "agent_name": "Technical Analyst",
            "stance": "Neutral",
            "reasoning": f"API Call Failed: {str(e)}",
            "confidence_score": 0.0
        }
