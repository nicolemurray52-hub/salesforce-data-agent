from __future__ import annotations

from src.metrics import SalesforceMetricsAgent


agent = SalesforceMetricsAgent()


def ask(question: str):
    return agent.answer(question)

