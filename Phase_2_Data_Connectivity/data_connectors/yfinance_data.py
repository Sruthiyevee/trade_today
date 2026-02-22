import yfinance as yf
import logging

logger = logging.getLogger("yfinance_data")

def fetch_live_ohlcv(ticker: str) -> dict:
    """
    Fetches real-time (last traded) OHLCV data for a given ticker using Yahoo Finance.
    For NSE stocks, the ticker must have a '.NS' suffix (e.g. RELIANCE.NS).
    """
    logger.info(f"Fetching real OHLCV data from yfinance for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        
        # Get historical data for the last 5 days to compute short-term trends if needed
        hist = stock.history(period="5d")
        
        if hist.empty:
            logger.warning(f"No yfinance data found for {ticker}")
            return {"error": "No market data available"}
            
        latest = hist.iloc[-1]
        
        return {
            "ticker": ticker,
            "current_price": float(latest["Close"]),
            "open": float(latest["Open"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "volume": int(latest["Volume"])
        }
        
    except Exception as e:
        logger.error(f"yfinance fetch failed for {ticker}: {str(e)}")
        return {"error": str(e)}
