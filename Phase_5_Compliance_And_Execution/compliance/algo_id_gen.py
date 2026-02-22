import hashlib
import time
import logging

logger = logging.getLogger("algo_id_gen")

def generate_algo_id(ticker: str, stance: str) -> str:
    """
    Generates a unique, SEBI-style algorithmic order ID. 
    This is critical for mapping an executed trade on a free broker API 
    directly back to the specific LLM consensus run.
    """
    timestamp = str(time.time()).encode('utf-8')
    core_string = f"{ticker}_{stance}_".encode('utf-8') + timestamp
    
    hash_object = hashlib.sha256(core_string)
    # Return a 15-character prefix of the hash to append to broker orders
    algo_signature = f"AI_{hash_object.hexdigest()[:12].upper()}"
    
    logger.debug(f"Generated Audit ID: {algo_signature} for {ticker}")
    return algo_signature
