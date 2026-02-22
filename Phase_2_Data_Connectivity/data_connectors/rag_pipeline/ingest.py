"""
RAG Pipeline: Pure-Python Vector Store (No C++ required)
─────────────────────────────────────────────────────────
Architecture:
  - Embeddings: SentenceTransformers 'all-MiniLM-L6-v2' (CPU-friendly, free)
  - Vector Store: Local SQLite with numpy cosine similarity (no ChromaDB/faiss needed)
  - Data Source: yfinance live financial metadata + Yahoo Finance summaries
"""
import os
import sys
import json
import sqlite3
import logging
import numpy as np
import yfinance as yf
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("rag_pipeline")

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_BASE, "vector_store.db")

# ─────────────────────────────────────────────
# Model (loaded once)
# ─────────────────────────────────────────────
_EMBED_MODEL = None

def _get_embed_model():
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        logger.info("Loading SentenceTransformer (all-MiniLM-L6-v2)...")
        _EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _EMBED_MODEL

# ─────────────────────────────────────────────
# SQLite Vector Store helpers
# ─────────────────────────────────────────────
def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id TEXT PRIMARY KEY,
            ticker TEXT,
            chunk_text TEXT,
            embedding BLOB
        )
    """)
    conn.commit()
    conn.close()

def _upsert_chunk(chunk_id: str, ticker: str, text: str, embedding: np.ndarray):
    conn = sqlite3.connect(DB_PATH)
    embedding_bytes = embedding.astype(np.float32).tobytes()
    conn.execute(
        "INSERT OR REPLACE INTO embeddings (id, ticker, chunk_text, embedding) VALUES (?, ?, ?, ?)",
        (chunk_id, ticker, text, embedding_bytes)
    )
    conn.commit()
    conn.close()

def _fetch_all_for_ticker(ticker: str):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, chunk_text, embedding FROM embeddings WHERE ticker = ?", (ticker,)
    ).fetchall()
    conn.close()
    
    results = []
    for row_id, text, emb_bytes in rows:
        emb = np.frombuffer(emb_bytes, dtype=np.float32)
        results.append((row_id, text, emb))
    return results

def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

# ─────────────────────────────────────────────
# Ingest
# ─────────────────────────────────────────────
def ingest_stock_fundamentals(ticker: str) -> dict:
    """
    Pulls live financial data from yfinance, creates text chunks,
    embeds with SentenceTransformers and stores in local SQLite.
    """
    logger.info(f"Ingesting fundamental data for {ticker} into Vector Store...")
    _init_db()
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        name = info.get("longName", ticker)
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        pb_ratio = info.get("priceToBook", "N/A")
        eps = info.get("trailingEps", "N/A")
        revenue = info.get("totalRevenue", "N/A")
        profit_margin = info.get("profitMargins", "N/A")
        debt_equity = info.get("debtToEquity", "N/A")
        roe = info.get("returnOnEquity", "N/A")
        dividend_yield = info.get("dividendYield", "N/A")
        beta = info.get("beta", "N/A")
        week52_high = info.get("fiftyTwoWeekHigh", "N/A")
        week52_low = info.get("fiftyTwoWeekLow", "N/A")
        analyst_target = info.get("targetMeanPrice", "N/A")
        recommendation = info.get("recommendationKey", "N/A")
        business_summary = info.get("longBusinessSummary", "")
        
        chunks = [
            f"{name} ({ticker}) operates in the {sector} sector ({industry}). "
            f"Market Cap: {market_cap}. Beta: {beta}. "
            f"52-week range: {week52_low} to {week52_high}.",
            
            f"{name} valuation: P/E Ratio: {pe_ratio}, "
            f"Price-to-Book: {pb_ratio}, EPS: {eps}. "
            f"Analyst target price: {analyst_target}. Recommendation: {recommendation}.",
            
            f"{name} financial health: Revenue: {revenue}, "
            f"Profit Margin: {profit_margin}, Debt-to-Equity: {debt_equity}, "
            f"ROE: {roe}, Dividend Yield: {dividend_yield}.",
        ]
        
        if business_summary:
            chunks.append(f"{name} business overview: {business_summary[:1200]}")
        
        model = _get_embed_model()
        embeddings = model.encode(chunks)
        
        for i, (text, embedding) in enumerate(zip(chunks, embeddings)):
            _upsert_chunk(f"{ticker}_chunk_{i}", ticker, text, embedding)
        
        logger.info(f"Ingested {len(chunks)} chunks for {ticker}.")
        return {"status": "success", "chunks_processed": len(chunks)}
        
    except Exception as e:
        logger.error(f"Ingest failed for {ticker}: {str(e)}")
        return {"status": "error", "error": str(e)}

# ─────────────────────────────────────────────
# Retrieve: Semantic Search
# ─────────────────────────────────────────────
def query_fundamentals(ticker: str, query: str, n_results: int = 3) -> str:
    """
    Embeds the query and retrieves the top-k most semantically similar
    chunks from the local SQLite vector store for the given ticker.
    """
    logger.info(f"RAG Query for [{ticker}]: '{query}'")
    _init_db()
    
    try:
        rows = _fetch_all_for_ticker(ticker)
        
        if not rows:
            logger.warning(f"No stored data for {ticker}. Triggering auto-ingest...")
            ingest_stock_fundamentals(ticker)
            rows = _fetch_all_for_ticker(ticker)
            
        if not rows:
            return f"No fundamental data available for {ticker}."
        
        model = _get_embed_model()
        query_embedding = model.encode([query])[0]
        
        # Rank by cosine similarity
        scored = [
            (text, _cosine_similarity(query_embedding, emb))
            for _, text, emb in rows
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        top_chunks = [text for text, _ in scored[:n_results]]
        return "\n\n".join(top_chunks)
        
    except Exception as e:
        logger.error(f"RAG query failed: {str(e)}")
        return f"RAG retrieval error: {str(e)}"

# ─────────────────────────────────────────────
# Standalone test
# ─────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_ticker = sys.argv[1] if len(sys.argv) > 1 else "RELIANCE.NS"
    
    print(f"\n[STEP 1] Ingesting {test_ticker}...")
    result = ingest_stock_fundamentals(test_ticker)
    print(f"Result: {result}")
    
    print(f"\n[STEP 2] Querying for financials...")
    ctx = query_fundamentals(test_ticker, "What is the valuation, P/E ratio, and financial health?")
    print(f"\nRetrieved Context:\n{ctx}")
