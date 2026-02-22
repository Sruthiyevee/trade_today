import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP Server
mcp = FastMCP("Financial News Scraper")

@mcp.tool()
def fetch_stock_news(ticker: str) -> str:
    """
    Fetches the 5 most recent financial news headlines for a given stock ticker 
    by scraping Yahoo Finance securely.
    """
    cleaned_ticker = ticker.replace(".NS", "")
    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Yahoo finance news headlines are usually currently in h3 tags with specific classes, 
        # but a general 'h3' tag search within the news container usually suffices for a basic free scraper.
        headlines = []
        for h3 in soup.find_all('h3', class_='clamp'):
            text = h3.get_text(strip=True)
            if text and text not in headlines:
                headlines.append(text)
                
        if not headlines:
            # Fallback for standard h3s if class changed
            for h3 in soup.find_all('h3'):
                text = h3.get_text(strip=True)
                if len(text) > 15 and text not in headlines:
                    headlines.append(text)
                    
        # Return top 5 headlines as a formatted string for the LLM
        if not headlines:
            return f"No recent news found for {ticker}."
            
        formatted_news = "\n".join([f"- {h}" for h in headlines[:5]])
        return f"Latest Headlines for {ticker}:\n{formatted_news}"
        
    except Exception as e:
        return f"Error scraping news for {ticker}: {str(e)}"

if __name__ == "__main__":
    # When run directly, it exposes the stdio server bindings for Langchain/Cursor to connect to
    mcp.run()
