import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger("audit_logger")

DB_PATH = os.path.join(os.path.dirname(__file__), "audit_logs.db")

def init_db():
    """Initializes the completely free local SQLite database for compliance trailing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            algo_id TEXT UNIQUE,
            ticker TEXT,
            action TEXT,
            rejection_reason TEXT,
            executed BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()
    logger.debug("Audit Database Initialized.")

def log_execution(algo_id: str, ticker: str, action: str, executed: bool, rejection_reason: str = ""):
    """Writes the graph outcome to the immutable local log."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        cursor.execute(
            '''INSERT INTO executions (timestamp, algo_id, ticker, action, rejection_reason, executed) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (timestamp, algo_id, ticker, action, rejection_reason, executed)
        )
        
        conn.commit()
        conn.close()
        logger.info(f"Successfully logged Algo ID {algo_id} to local DB.")
        
    except Exception as e:
        logger.error(f"Failed to log execution to SQLite: {str(e)}")

# Ensure the DB is created on import
init_db()
