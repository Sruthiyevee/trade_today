import os
import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger("sentiment_agent")

def run_sentiment_analysis(ticker: str, news_data: dict) -> dict:
    """
    Simulates the Sentiment Analyst Agent (SAA).
    In production, this node connects to an MCP Server to scrape financial news,
    then uses Groq-hosted Llama 3 to determine Market Mood.
    """
    logger.info(f"Running Sentiment Agent on {ticker} using Groq Llama 3...")
    
    api_key = os.getenv("GROQ_API_KEY", "dummy_key")
    if api_key == "dummy_key":
        logger.warning("No GROQ_API_KEY found, returning mock sentiment analysis.")
        return {
            "agent_name": "Sentiment Analyst",
            "stance": "Neutral",
            "reasoning": "API Call Failed (Missing Key) - Fallback Mock: Mixed news regarding recent regulatory changes, but strong consumer trust remains.",
            "confidence_score": 0.65
        }
        
    try:
        # Utilizing fast Llama 3 8B model for rapid sentiment classification
        llm = ChatGroq(temperature=0.2, model_name="llama-3.1-8b-instant")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Financial Sentiment Analyst focusing on the Indian market. Read the provided news headlines/summaries and output a purely sentiment-based stance (Bullish/Bearish/Neutral) along with a short 1-sentence reasoning."),
            ("human", "Assess the market mood for {ticker} based on this news data: {data}")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"ticker": ticker, "data": news_data})
        
        return {
            "agent_name": "Sentiment Analyst",
            "stance": "Derived via LLM",
            "reasoning": str(response.content),
            "confidence_score": 0.80 # Typically derived from confidence parsing or logprobs
        }
        
    except Exception as e:
        logger.error(f"Sentiment Agent failed: {str(e)}")
        return {
            "agent_name": "Sentiment Analyst",
            "stance": "Neutral",
            "reasoning": f"API Call Failed: {str(e)}",
            "confidence_score": 0.0
        }
