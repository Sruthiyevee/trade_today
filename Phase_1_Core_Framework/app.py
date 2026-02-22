import uvicorn
from fastapi import FastAPI
from api.routes import router as analyze_router
import logging

# Set up basic logging for uvicorn
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trade_today_app")

# Initialize the Backend Web Layer
app = FastAPI(
    title="Multi-Factor Trading Analyst API",
    description="Agentic framework mapping LangGraph logic to HTTP endpoints.",
    version="1.0.0"
)

# Connect Endpoint routes
app.include_router(analyze_router)

@app.get("/health")
async def root():
    """Simple healthcheck."""
    return {"status": "ok", "message": "Trading Analyst Backend Online"}

if __name__ == "__main__":
    logger.info("Starting Multi-Factor Trading Analyst Development Server...")
    # Bind to localhost port 8000
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
