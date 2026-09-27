# Salesforce Data Analysis Agent

A Python starter project for a Salesforce analytics agent that can answer business questions about:
- sales pipeline by opportunity stage
- lead conversion and source performance
- case backlog by status
- monthly revenue trend
- high-value accounts or opportunities

This project is designed as a foundation for a natural-language report agent over Salesforce data.

## What it includes

- Salesforce API connection via `simple-salesforce`
- reusable query helpers for opportunities, leads, and cases
- metric aggregation with pandas
- a lightweight agent that answers common sales questions
- environment-based configuration with `.env`

## Project structure

```text
salesforce-data-agent/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── salesforce_client.py
│   ├── metrics.py
│   └── agent.py
└── .gitignore
```

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment template and fill it in:

```bash
cp .env.example .env
```

4. Set your Salesforce credentials and optional OpenAI API key in `.env`.

## Required environment variables

```env
SF_USERNAME=your_username@example.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_LOGIN_URL=https://login.salesforce.com
OPENAI_API_KEY=your_openai_key_if_using_llm_summarization
```

## Example usage

```bash
python app.py
```

This will run a few sample questions against Salesforce data, including:
- pipeline summary
- lead conversion rate
- open cases by status

## Example questions to ask the agent

- What is the pipeline by stage?
- How many leads converted this quarter?
- What is our lead conversion rate?
- Which opportunities are highest value?
- How many open cases by status?
- What is our monthly revenue trend?

## Notes

- This starter project uses simple SOQL queries and pandas-based reporting.
- It is intentionally modular so you can add more Salesforce objects and more advanced dashboards later.
- For production use, add:
  - OAuth or connected app auth
  - retry logic
  - caching
  - production-grade validation
  - scheduled reports or API endpoints

## Next enhancements

- add FastAPI endpoints
- add CSV/JSON export
- add dashboard charts in Streamlit
- add Slack or Teams integration
- add agent routing with LangChain or LangGraph

