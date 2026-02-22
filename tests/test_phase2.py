import os
import sys

# Ensure the root of Phase 2 is in the python path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root, "Phase_2_Data_Connectivity"))

from data_connectors.news_scraper import get_basic_sentiment
from data_connectors.rag_pipeline.ingest import ingest_nse_pdf, query_fundamentals
from data_connectors.broker_api import FreeBrokerConnector

def run_tests():
    print("\n--- Testing Phase 2: Data Connectors & Boilerplates ---")
    
    # 1. Test Sentiment Scraper
    print("\n[1] Testing News Scraper:")
    sentiment = get_basic_sentiment("RELIANCE.NS")
    assert isinstance(sentiment, float), "Sentiment should be a float."
    print(f"-> Sentiment for RELIANCE.NS: {sentiment}")
    
    # 2. Test RAG Pipeline Ingestion Stub
    print("\n[2] Testing RAG Ingestion Pipeline:")
    ingest_result = ingest_nse_pdf("./dummy/annual_report.pdf", "RELIANCE.NS")
    assert ingest_result["status"] == "success", "RAG Ingestion status should be success."
    print(f"-> Ingestion Result: {ingest_result}")
    
    # 3. Test RAG Pipeline Query Stub
    print("\n[3] Testing RAG Querying:")
    query_result = query_fundamentals("RELIANCE.NS", "What was the revenue growth?")
    assert isinstance(query_result, str), "RAG query should return a string."
    print(f"-> Query Result: {query_result}")
    
    # 4. Test Free Broker API Connector
    print("\n[4] Testing Free Broker Connector (Mock Execution):")
    # Setting mock env vars to simulate auth
    os.environ['BROKER_ID'] = 'test_id'
    os.environ['BROKER_SECRET'] = 'test_secret'
    
    connector = FreeBrokerConnector()
    order_result = connector.execute_limit_order("RELIANCE.NS", "BUY", 10, 2500.50)
    assert order_result["status"] == "success", "Broker order should succeed."
    assert "order_id" in order_result, "Broker response must include order_id."
    print(f"-> Broker Result: {order_result}\n")
    
    print("-> All Phase 2 tests passed successfully.\n")

if __name__ == "__main__":
    run_tests()
