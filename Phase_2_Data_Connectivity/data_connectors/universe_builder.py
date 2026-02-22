import os
import io
import json
import logging
import requests
import pandas as pd

logger = logging.getLogger("universe_builder")
logging.basicConfig(level=logging.INFO)

UNIVERSE_PATH = os.path.join(os.path.dirname(__file__), "ticker_universe.json")

def fetch_nse_universe() -> list:
    """Fetches the official NSE equity list and formats them for yfinance (.NS)"""
    logger.info("Fetching NSE Equity List...")
    url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        
        df = pd.read_csv(io.StringIO(res.text))
        
        tickers = []
        for _, row in df.iterrows():
            symbol = str(row.get('SYMBOL', '')).strip()
            name = str(row.get('NAME OF COMPANY', '')).strip()
            if symbol and name:
                tickers.append({
                    "ticker": f"{symbol}.NS",
                    "name": name,
                    "exchange": "NSE"
                })
        
        logger.info(f"Successfully parsed {len(tickers)} NSE stocks.")
        return tickers
        
    except Exception as e:
        logger.error(f"Failed to fetch NSE universe: {str(e)}")
        return []

def build_market_universe():
    """Compiles all tickers and saves to a local JSON for the UI to load."""
    universe = []
    
    nse_stocks = fetch_nse_universe()
    universe.extend(nse_stocks)
    
    # BSE scraping dynamically from the List_Scrips.html requires a headless browser or POST request 
    # to bypass the ASP.NET form. For a free architecture, users can optionally place a downloaded 
    # BSE Equity.csv in this folder.
    bse_csv_path = os.path.join(os.path.dirname(__file__), "BSE_Equity.csv")
    if os.path.exists(bse_csv_path):
        logger.info("Found local BSE_Equity.csv. Parsing...")
        try:
            bse_df = pd.read_csv(bse_csv_path)
            # Assuming standard BSE CSV format with 'Security Code' and 'Security Name'
            for _, row in bse_df.iterrows():
                code = str(row.get('Security Code', '')).strip()
                name = str(row.get('Security Name', '')).strip()
                if code and name:
                    universe.append({
                        "ticker": f"{code}.BO",
                        "name": name,
                        "exchange": "BSE"
                    })
            logger.info("Successfully parsed BSE stocks.")
        except Exception as e:
            logger.error(f"Failed to parse BSE CSV: {str(e)}")
    else:
        logger.warning("No local BSE_Equity.csv found. Skipping BSE.")
        
    # Save the consolidated list
    with open(UNIVERSE_PATH, 'w', encoding='utf-8') as f:
        json.dump(universe, f, indent=4)
        
    logger.info(f"Market Universe built successfully! Total Stocks: {len(universe)}")
    logger.info(f"Saved to: {UNIVERSE_PATH}")

if __name__ == "__main__":
    build_market_universe()
