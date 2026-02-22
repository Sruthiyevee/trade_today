import streamlit as st
import time
import random
import hashlib
import yfinance as yf
import json
import os

@st.cache_data
def load_universe():
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        universe_path = os.path.join(root_dir, "Phase_2_Data_Connectivity", "data_connectors", "ticker_universe.json")
        if os.path.exists(universe_path):
            with open(universe_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading universe: {e}")
    return []

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
    
    *(Note: This dashboard is currently running in **Simulation Mode** while the backend APIs are finalized. Responses are simulated based on the ticker you enter!)*
    """)
    
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

if __name__ == "__main__":
    main()
