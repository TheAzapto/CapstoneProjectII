# Financial News Sentiment Analyzer

Link to Website: [Finnalyze](https://finnalyze.vercel.app)

## Overview

This project is a Financial News Sentiment Analyzer designed to scrape financial news articles, summarize their content, and evaluate the potential market impact on specific companies. It leverages a local Large Language Model (LLM), specifically a fine-tuned version of Llama 3.1 (`fin-llama3.1-8b`), to perform advanced natural language processing tasks tailored for the financial domain.

## Features

- **News Scraping**: Automatically scrapes the latest financial news headlines and articles from LiveMint.
- **Article Summarization**: Generates concise, one-sentence summaries of financial articles, focusing on core financial topics and events.
- **Sentiment & Impact Analysis**: Evaluates the summarized text to assign impact scores (from -1.0 to 1.0) to mentioned companies, reflecting the potential effect on their stock performance.
- **REST API**: Provides a Flask-based REST API endpoint (`/analyze`) to process articles and return impact scores in JSON format.
- **Middleware Integration**: Uses a dedicated middleware to interface with the local Ollama LLM instance.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**: The programming language used for the backend.
- **Ollama**: A tool for running LLMs locally.
- **FinLlama Model**: You need to pull the specific model used in this project:

  ```bash
  ollama pull hf.co/us4/fin-llama3.1-8b:Q5_K_M
  ```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.
2. **Install Python dependencies**:
    It is recommended to use a virtual environment.

    ```bash
    pip install virtualenv
    virtualenv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Usage

### 1. Start the Backend Server

The Flask application serves as the API for analyzing articles.

```bash
python backend/app.py
```

The server will start on `http://localhost:5000`.

### 2. Run the News Scraper

The scraper fetches the latest news and sends it to the backend for analysis.

```bash
python backend/LLM_Files/NewsScrapper.py
```

This script will:

1. Scrape the latest article link from LiveMint.
2. Extract the article content.
3. Send the content to the running Flask API.
4. Print the JSON response containing company names and their impact scores.

Key Cybersecurity Risk
Web Scraping Risks
IP blocking/rate limiting - Aggressive scraping can get your IP banned from news sources
Legal exposure - Some sites prohibit scraping in their Terms of Service, potentially leading to CFAA violations
Malicious content injection - Scraped sites could contain XSS payloads or malware if not properly sanitized
Data poisoning - Scraped content could be manipulated by attackers to influence your model's predictions
Model & Data Risks
Training data poisoning - If scraping from public sources, attackers could plant misleading articles to bias your model
Model theft - Fine-tuned models represent valuable IP; unauthorized access to your Ollama instance could expose them
Prompt injection - If users can input queries, they might manipulate the model to produce harmful outputs or leak training data
Overfitting on manipulated data - Market manipulation attempts in news could skew your sentiment analysis
Infrastructure Risks
Exposed Ollama API - Default Ollama setup listens on localhost, but if exposed to network without authentication, anyone can query/modify models
Credential exposure - API keys for news sources, database passwords, or cloud credentials in code/config files
Dependency vulnerabilities - Python libraries for scraping (BeautifulSoup, Scrapy) and ML (transformers, etc.) may have known CVEs
Resource exhaustion - Ollama models are resource-intensive; DoS attacks could overwhelm your system
Data Privacy & Compliance
PII in scraped content - News articles might contain personal information requiring GDPR/CCPA compliance
Financial data regulations - Depending on jurisdiction, providing financial analysis may require licensing
Data retention - Storing historical news data creates liability if breached
Mitigation Recommendations
Scraping Security
Use official APIs where available instead of scraping
Implement proper rate limiting and respect robots.txt
Sanitize all scraped HTML to prevent XSS
Validate data integrity before feeding to model
Use rotating proxies/user agents responsibly
Model Protection
Keep Ollama API on localhost or behind authentication
Implement input validation and output filtering
Version control your models and monitor for unauthorized changes
Consider adversarial training to resist poisoned inputs
Infrastructure Hardening
Use environment variables for all credentials
Regularly update dependencies (run pip audit)
Implement request throttling if exposing any APIs
Run services in containers with minimal privileges
Set up monitoring for unusual resource usage
Operational Security
Don't store raw API keys in git repositories
Log all data sources for audit trails
Implement circuit breakers for scraping failures
Have incident response plan for model manipulation detection




- `backend/app.py`: The Flask API server handling analysis requests.
- `backend/FinLlama_Middleware.py`: Contains functions `Summarize` and `Evaluate` that interact with the Ollama LLM.
- `backend/NewsScrapper.py`: Script to scrape news and trigger analysis.
- `backend/StockNames.csv`: A CSV file containing a list of stock names (used by the middleware).
