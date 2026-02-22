import os
import logging

try:
    from langfuse.callback import CallbackHandler
except Exception as e:
    CallbackHandler = None
    logging.warning(f"Langfuse library failed to import (likely Pydantic v1 / Py3.14 issue): {e}")

logger = logging.getLogger("langfuse_config")

def get_langfuse_handler():
    """
    Initializes the Langfuse callback handler for instrumenting LangGraph node executions.
    This acts as our 100% free LangSmith replacement running on a local Docker container or
    the Oracle Free-Tier VM.
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "dummy_pk")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "dummy_sk")
    host = os.getenv("LANGFUSE_HOST", "http://localhost:3000") # Default self-hosted port
    
    if public_key == "dummy_pk":
        logger.warning("No LANGFUSE_PUBLIC_KEY found. Running Orchestrator without local telemetry.")
        return None
        
    logger.info(f"Connecting to self-hosted Langfuse at {host}...")
    try:
        langfuse_handler = CallbackHandler(
            public_key=public_key,
            secret_key=secret_key,
            host=host
        )
        return langfuse_handler
    except Exception as e:
        logger.error(f"Failed to initialize Langfuse Callback: {str(e)}")
        return None
