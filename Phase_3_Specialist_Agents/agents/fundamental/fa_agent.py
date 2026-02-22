import os
import sys
import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Inject Phase 2 path so we can access the RAG pipeline
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_phase2 = os.path.join(_root, "Phase_2_Data_Connectivity")
if _phase2 not in sys.path:
    sys.path.insert(0, _phase2)

from data_connectors.rag_pipeline.ingest import ingest_stock_fundamentals, query_fundamentals

logger = logging.getLogger("fa_agent")

def run_fundamental_analysis(ticker: str, rag_context: str = "") -> dict:
    """
    The Fundamental Analyst Agent (FAA) — Groq + RAG Edition.

    Execution flow:
    1. Ingest fresh fundamentals for the ticker from yfinance → stores in SQLite vector store.
    2. Retrieve the most semantically relevant chunks via cosine similarity (RAG).
    3. Pass the retrieved context to Groq Llama 3 for a grounded, non-hallucinated analysis.
    """
    logger.info(f"Running FAA on {ticker} using Groq Llama 3 + local RAG...")
    
    # ─── STEP 1: Ingest freshest fundamentals into vector store ───
    logger.info(f"Triggering RAG ingest for {ticker}...")
    ingest_result = ingest_stock_fundamentals(ticker)
    logger.info(f"Ingest result: {ingest_result}")
    
    # ─── STEP 2: Retrieve relevant context via semantic search ───
    retrieved_context = query_fundamentals(
        ticker,
        "valuation, P/E ratio, revenue, profitability, debt, financial health, analyst recommendation"
    )
    logger.info(f"RAG context retrieved ({len(retrieved_context)} chars).")
    
    # ─── STEP 3: Synthesize with Groq Llama 3 ───
    api_key = os.getenv("GROQ_API_KEY", "dummy_key")
    
    if api_key == "dummy_key":
        logger.warning("No GROQ_API_KEY found. Returning raw RAG context without LLM synthesis.")
        return {
            "agent_name": "Fundamental Analyst",
            "stance": "Neutral",
            "reasoning": (
                "API Call Failed (Missing GROQ Key) — RAG context retrieved but not synthesized:\n\n"
                + retrieved_context[:500]
            ),
            "confidence_score": 0.50
        }
    
    try:
        llm = ChatGroq(
            api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.2
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a conservative, data-driven Fundamental Analyst for the Indian Equity Market. "
             "You have been provided with retrieved financial data from a RAG knowledge base. "
             "Analyze ONLY the provided data. Do NOT hallucinate any numbers. "
             "Provide: (1) A one-word stance: Bullish, Bearish, or Neutral. "
             "(2) A concise 2-3 sentence reasoning that cites specific metrics from the context."),
            ("human",
             "Company: {ticker}\n\n"
             "Retrieved Financial Context (from RAG):\n{context}\n\n"
             "Provide your fundamental analysis stance and reasoning based strictly on the above data.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({
            "ticker": ticker,
            "context": retrieved_context
        })
        
        response_text = str(response.content)
        
        # Parse the stance from the LLM's response
        stance = "Neutral"
        if "bullish" in response_text.lower():
            stance = "Bullish"
        elif "bearish" in response_text.lower():
            stance = "Bearish"
        
        return {
            "agent_name": "Fundamental Analyst",
            "stance": stance,
            "reasoning": response_text,
            "confidence_score": 0.85
        }
        
    except Exception as e:
        logger.error(f"FAA Groq call failed: {str(e)}")
        return {
            "agent_name": "Fundamental Analyst",
            "stance": "Neutral",
            "reasoning": (
                f"API Call Failed: {str(e)}\n\n"
                f"RAG Context (unsynthesized):\n{retrieved_context[:400]}"
            ),
            "confidence_score": 0.0
        }
