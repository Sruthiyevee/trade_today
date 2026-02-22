Hhere is an architecture for an agentic Multi-Factor Trading Analyst designed for the Indian equity market (NSE and BSE), utilizing exclusively free, open-source, or strictly free-tier tools.

1. Core Tech Stack and Orchestration
The system represents a shift from static querying to a stateful, autonomous workflow using a hub-and-spoke multi-agent architecture powered by zero-cost tools.


Python: Serves as the primary computational language for handling asynchronous pipelines and data calculations.


LangGraph: Acts as the orchestration engine, utilizing StateGraph and conditional edges to manage iterative reasoning loops, workflow routing, and durable execution (checkpoints to resume after failures via local SQLite).


LangChain: Functions as the connectivity framework, utilizing AgentExecutor and ToolNode to define node functions and link agents to tools.


State Management: The shared memory of the system, carrying user intent and aggregated research, is implemented using Python TypedDict or Pydantic models.

2. Specialist Agents and Roles
The architecture breaks down market analysis into specialized nodes that mimic a professional investment committee, powered by open-weight or free-tier LLMs like Llama 3 via Groq.


Portfolio Manager (Lead Analyst): Acts as the central hub that orchestrates the workflow, plans execution strategies, and coordinates data flow. It synthesizes the final trading advice (Buy, Sell, or Hold) through a consensus mechanism after evaluating all risk factors.


Technical Analyst Agent (TAA): Forecasts short-term price movements using historical OHLCV data. It utilizes open-source Python libraries like TA-Lib to compute indicators common in the Indian market, such as RSI, MACD, and Bollinger Bands.


Fundamental Analyst Agent (FAA): Focuses on quantitative extraction from financial statements. It calculates metrics like P/E ratios, Return on Equity (ROE), and debt-to-equity, utilizing a multi-stage Retrieval-Augmented Generation (RAG) pipeline to ingest dense NSE corporate filings into a local ChromaDB instance utilizing Gemini 1.5 Flash (via free API limits).


Sentiment Analyst Agent (SAA): Evaluates qualitative market behavior, such as management credibility from earnings calls and headlines. A primary approach is building custom web scrapers (BeautifulSoup) for free financial news endpoints to map fear/greed metrics.


Bull and Bear Researchers: Engaged by the Portfolio Manager in a "Structured Adversarial Synthesis". The Bull agent builds the optimistic growth narrative, while the Bear agent stress-tests the logic by identifying structural risks and overvaluations.


Risk Manager: Monitors portfolio exposure limits, liquidity, and volatility constraints locally.

3. Integrations and Connectivity
The system relies on the Model Context Protocol (MCP) to standardize communication across the fragmented Indian brokerage ecosystem, strictly avoiding paid API barriers.


MCP via langchain-mcp-adapters: Transforms various zero-cost data sources and execution venues into interchangeable tools that the agents can use without hardcoding specific API rules.


Broker APIs (Execution & Price Data): Connects to free brokers like Dhan, Finvasia Shoonya, or Fyers for live streaming prices and order execution (e.g., execute_limit_order) without API charges.


Fundamental Data & News: Generates custom MCP servers wrapping zero-cost BeautifulSoup and Selenium scrapers targeting free domains.


RAG & Document Processing: Uses Docling to convert free PDF annual reports (NSE filings) into structured Markdown. It stores these in ChromaDB (open-source) and queries via Gemini 1.5 Flash (free tier) to extract precise numerical context.


Monitoring: Integrated with Langfuse (self-hosted open-source version) to provide deep, zero-cost visibility into the agentic workflow, trace the logic of the Bull vs. Bear debate, and monitor token usage.

4. User Interface and Application Layer

FastAPI & Streamlit: The backend operational layer is built using a low-latency, asynchronous FastAPI pipeline, communicating with an entirely open-source Streamlit frontend.


Token Streaming: WebSockets are used to provide a bidirectional communication layer to the UI. This enables real-time "token streaming" to the frontend, allowing the user to watch the agent's reasoning processes, debates, and price updates live, reducing perceived latency.

5. Regulatory Compliance Layer (SEBI)
Crucially, the architecture must align with SEBI and NSE automated trading mandates for 2025/2026. The implementation must include:

A unique "Algo ID" for every generated order and rigorous audit trails linking trades back to the agent's research, securely stored in a local PostgreSQL database.

Static IP whitelisting (utilizing Oracle's Always Free Tier servers), mandatory 2FA, and an emergency broker kill-switch.

Registration as a Research Analyst (RA) for proprietary "Black Box" AI logic through generated audit trails.