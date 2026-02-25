import streamlit as st
import time
import random
import hashlib
import yfinance as yf
import io
import requests
import pandas as pd

NSE_EQUITY_URL = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

FALLBACK_STOCKS = [
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries Limited"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Services"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank Limited"},
    {"ticker": "INFY.NS", "name": "Infosys Limited"},
    {"ticker": "ICICIBANK.NS", "name": "ICICI Bank Limited"},
    {"ticker": "HINDUNILVR.NS", "name": "Hindustan Unilever Limited"},
    {"ticker": "ITC.NS", "name": "ITC Limited"},
    {"ticker": "SBIN.NS", "name": "State Bank of India"},
    {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel Limited"},
    {"ticker": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank Limited"},
    {"ticker": "WIPRO.NS", "name": "Wipro Limited"},
    {"ticker": "AXISBANK.NS", "name": "Axis Bank Limited"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro Limited"},
    {"ticker": "ASIANPAINT.NS", "name": "Asian Paints Limited"},
    {"ticker": "MARUTI.NS", "name": "Maruti Suzuki India Limited"},
]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_universe():
    """Fetch the live NSE equity list from the official NSE CSV.
    Falls back to a hardcoded list of major stocks if the download fails."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        res = requests.get(NSE_EQUITY_URL, headers=headers, timeout=10)
        res.raise_for_status()
        df = pd.read_csv(io.StringIO(res.text))
        stocks = []
        for _, row in df.iterrows():
            symbol = str(row.get('SYMBOL', '')).strip()
            name = str(row.get('NAME OF COMPANY', '')).strip()
            if symbol and name:
                stocks.append({"name": name, "ticker": f"{symbol}.NS"})
        if stocks:
            return stocks
    except Exception as e:
        st.warning(f"Could not fetch live NSE stock list (using fallback): {e}")
    return FALLBACK_STOCKS

# Basic configuration
st.set_page_config(
    page_title="Multi-Factor Trading Analyst",
    page_icon="📈",
    layout="wide"
)

def generate_mock_data(ticker):
    # Seed random with ticker to get consistent but varying results for different tickers
    random.seed(ticker + str(time.time())[:5]) # slight variation over time, but generally varied
    
    decisions = ["BUY", "SELL", "HOLD"]
    decision = random.choices(decisions, weights=[0.4, 0.4, 0.2])[0]
    
    confidences = ["High Confidence", "Medium Confidence", "Low Confidence"]
    confidence = random.choice(confidences)
    
    # Generate mock IDs
    hash_str = f"{ticker}_{time.time()}"
    hash_object = hashlib.sha256(hash_str.encode('utf-8'))
    audit_id = f"AI_{hash_object.hexdigest()[:12].upper()}"
    order_id = f"MOCK_BROKER_{random.randint(100, 999)}" if decision != "HOLD" else "N/A"
    
    # Varied analyst text
    price_trends = [
        "Bullish (Short-term price momentum looks strong)",
        "Bearish (Recent moving averages indicate a downward trend)",
        "Neutral (Price is consolidating within a tight range)",
        "Bullish (Golden cross formation detected on the daily chart)"
    ]
    health = [
        "Neutral (Sales are growing, but the company still has some debt)",
        "Positive (Strong balance sheet with excellent quarterly earnings)",
        "Negative (Declining profit margins and high operational costs)",
        "Positive (Consistent dividend payouts and low debt-to-equity)"
    ]
    risks = [
        "Be careful, recent positive news might be exaggerated by social media.",
        "Market volatility is currently high for this specific sector.",
        "No major immediate red flags found in recent SEC/NSE filings.",
        "Beware of potential upcoming regulatory changes affecting this industry."
    ]
    
    return decision, confidence, audit_id, order_id, random.choice(price_trends), random.choice(health), random.choice(risks)

def main():
    st.title("📈 AI Stock Trading Assistant")
    st.markdown("""
    Welcome to your AI Stock Trading Assistant. 
    Simply enter a stock symbol below, and our team of AI analysts will research the company's financials, current news, and market trends to give you a clear trading decision.
    """)

    st.warning(
        "**Disclaimer:** The analysis and recommendations provided by this tool are "
        "**AI-generated suggestions only** and do **not** constitute financial advice, "
        "investment recommendations, or any form of regulated guidance. "
        "Always consult a qualified financial advisor before making investment decisions. "
        "Trade at your own risk."
    )
    
    universe = load_universe()
    if universe:
        options = [f"{item['name']} ({item['ticker']})" for item in universe]
        # Default to Reliance if it exists in the list
        default_index = 0
        for i, opt in enumerate(options):
            if "RELIANCE.NS" in opt:
                default_index = i
                break
                
        selected_display = st.selectbox("Search and Select a Stock:", options=options, index=default_index)
        
        # Extract just the ticker symbol from inside the parentheses
        if selected_display:
            ticker = selected_display.split('(')[-1].replace(')', '').strip()
        else:
            ticker = ""
    else:
        # Fallback if the JSON file wasn't built yet
        ticker = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, INFY.NS):", value="RELIANCE.NS").upper().strip()
    
    if ticker:
        with st.spinner(f"Fetching live market data for {ticker}..."):
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0.0))
                company_name = info.get('longName', ticker)
                
                # Fetch recent history for OHLCV
                hist = stock.history(period="1d")
                if not hist.empty:
                    latest = hist.iloc[-1]
                    open_px = latest["Open"]
                    high_px = latest["High"]
                    low_px = latest["Low"]
                    volume = latest["Volume"]
                else:
                    open_px, high_px, low_px, volume = 0.0, 0.0, 0.0, 0
                
                if current_price > 0:
                    st.subheader(f"📊 {company_name} ({ticker})")
                    
                    # Display Live OHLCV metrics
                    m1, m2, m3, m4, m5 = st.columns(5)
                    m1.metric("LTP (Live)", f"₹{current_price:,.2f}")
                    m2.metric("Open", f"₹{open_px:,.2f}")
                    m3.metric("High", f"₹{high_px:,.2f}")
                    m4.metric("Low", f"₹{low_px:,.2f}")
                    m5.metric("Volume", f"{int(volume):,}")
                    st.divider()
                else:
                    st.warning(f"Could not fetch complete live data for {ticker}. Please check the symbol.")
            except Exception as e:
                st.warning(f"Error fetching live data: {str(e)}")

    if st.button("Trigger AI Analysis"):
        if not ticker:
            st.error("Please enter a valid stock symbol.")
            return
            
        with st.spinner(f"Our AI team is researching {ticker}..."):
            # Mocking the pipeline duration
            time.sleep(2)
            
            # Generate dynamic mock data
            decision, confidence, audit_id, order_id, trend_text, health_text, risk_text = generate_mock_data(ticker)
            
            st.success("Analysis Complete! Action recommended.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Final Decision", value=decision, delta=confidence)
            with col2:
                st.metric(label="Regulatory Audit ID", value=audit_id)
            with col3:
                st.metric(label="Order ID", value=order_id)
            
            st.subheader("What Our AI Analysts Say:")
            
            # Use dynamic emojis based on stance
            trend_emoji = "📈" if "Bullish" in trend_text else "📉" if "Bearish" in trend_text else "➡️"
            health_emoji = "🟢" if "Positive" in health_text else "🔴" if "Negative" in health_text else "🟡"
            
            st.info(f"{trend_emoji} Price Trend Analyst: {trend_text}")
            st.info(f"{health_emoji} Company Health Analyst: {health_text}")
            
            st.subheader("Risk Check:")
            st.warning(f"⚠️ Risk Analyst: {risk_text}")

            st.divider()
            st.caption(
                "🔔 **This is a suggestion, not advice.** "
                "The above output is generated by AI models using simulated data and should not be treated as financial or investment advice. "
                "Please do your own research (DYOR) and consult a SEBI-registered investment advisor before acting on any recommendation."
            )

if __name__ == "__main__":
    main()
