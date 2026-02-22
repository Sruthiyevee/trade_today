import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger("fa_agent")

def run_fundamental_analysis(ticker: str, rag_context: str) -> dict:
    """
    Simulates the Fundamental Analyst Agent (FAA).
    This agent utilizes Google's Gemini 1.5 Flash due to its massive context window
    provided on the free tier, allowing it to synthesize dense local ChromaDB RAG pulls.
    """
    logger.info(f"Running FAA on {ticker} using Gemini 1.5 Flash...")
    
    api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
    if api_key == "dummy_key":
        logger.warning("No GEMINI_API_KEY found, returning mock fundamental analysis.")
        return {
            "agent_name": "Fundamental Analyst",
            "stance": "Neutral",
            "reasoning": "Mock: Quarterly revenue grew, but debt-to-equity ratio remains a concern.",
            "confidence_score": 0.60
        }
        
    # Real execution mapping
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a conservative Fundamental Analyst for the Indian Equity Market. Base your stance strictly on the provided RAG context."),
            ("human", "Company: {ticker}\nContext: {context}\nProvide your stance (Bullish/Bearish/Neutral) and reasoning.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"ticker": ticker, "context": rag_context})
        
        return {
            "agent_name": "Fundamental Analyst",
            "stance": "Derived via LLM",
            "reasoning": str(response.content),
            "confidence_score": 0.80
        }
        
    except Exception as e:
        logger.error(f"FAA failed: {str(e)}")
        return {}
