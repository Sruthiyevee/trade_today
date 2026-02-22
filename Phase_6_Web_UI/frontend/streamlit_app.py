import streamlit as st
import time
import random
import hashlib

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
    
    ticker = st.text_input("Enter Stock Symbol:", value="RELIANCE.NS").upper().strip()
    
    if st.button("Analyze Stock"):
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
