from __future__ import annotations

from typing import Dict, List

import pandas as pd

from src.salesforce_client import SalesforceClient


def _to_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def pipeline_by_stage() -> pd.DataFrame:
    records = SalesforceClient.get_opportunities()
    rows = []

    for record in records:
        rows.append(
            {
                "Stage": record.get("StageName"),
                "Amount": _to_float(record.get("Amount")),
                "CloseDate": record.get("CloseDate"),
                "Name": record.get("Name"),
                "Owner": record.get("Owner", {}).get("Name") if isinstance(record.get("Owner"), dict) else None,
            }
        )

    if not rows:
        return pd.DataFrame(columns=["Stage", "Amount", "CloseDate", "Name", "Owner"])

    df = pd.DataFrame(rows)
    grouped = df.groupby("Stage", dropna=False)["Amount"].sum().reset_index()
    grouped.columns = ["Stage", "Total_Amount"]
    return grouped.sort_values("Total_Amount", ascending=False)


def lead_conversion_rate() -> Dict[str, float | int]:
    records = SalesforceClient.get_leads()
    total = len(records)
    converted = sum(1 for r in records if bool(r.get("IsConverted")))

    rate = round((converted / total) * 100, 2) if total else 0.0
    return {
        "total_leads": total,
        "converted_leads": converted,
        "conversion_rate_pct": rate,
    }


def open_cases_by_status() -> pd.DataFrame:
    records = SalesforceClient.get_cases()
    rows = []

    for record in records:
        if not record.get("IsClosed"):
            rows.append({"Status": record.get("Status"), "Priority": record.get("Priority")})

    if not rows:
        return pd.DataFrame(columns=["Status", "Count"])

    df = pd.DataFrame(rows)
    grouped = df.groupby("Status", dropna=False).size().reset_index(name="Count")
    return grouped.sort_values("Count", ascending=False)


def revenue_trend() -> pd.DataFrame:
    records = SalesforceClient.get_opportunities()
    rows = []

    for record in records:
        close_date = record.get("CloseDate")
        if not close_date:
            continue
        rows.append({
            "CloseDate": pd.to_datetime(close_date, errors="coerce"),
            "Amount": _to_float(record.get("Amount")),
        })

    if not rows:
        return pd.DataFrame(columns=["Month", "Total_Amount"])

    df = pd.DataFrame(rows).dropna(subset=["CloseDate"])
    df["Month"] = df["CloseDate"].dt.to_period("M").astype(str)
    grouped = df.groupby("Month", as_index=False)["Amount"].sum()
    grouped.columns = ["Month", "Total_Amount"]
    return grouped.sort_values("Month")


def top_opportunities_by_value(limit: int = 10) -> pd.DataFrame:
    records = SalesforceClient.get_opportunities()
    rows = []

    for record in records:
        rows.append(
            {
                "Name": record.get("Name"),
                "Amount": _to_float(record.get("Amount")),
                "Stage": record.get("StageName"),
                "CloseDate": record.get("CloseDate"),
                "Owner": record.get("Owner", {}).get("Name") if isinstance(record.get("Owner"), dict) else None,
            }
        )

    if not rows:
        return pd.DataFrame(columns=["Name", "Amount", "Stage", "CloseDate", "Owner"])

    df = pd.DataFrame(rows)
    return df.sort_values("Amount", ascending=False).head(limit)


class SalesforceMetricsAgent:
    def answer(self, question: str) -> Dict[str, object]:
        q = question.lower()

        if "pipeline" in q or "stage" in q or "opportunity" in q:
            pipeline = pipeline_by_stage()
            return {
                "type": "pipeline_summary",
                "result": pipeline.to_dict(orient="records"),
            }

        if "lead" in q and ("conversion" in q or "converted" in q or "rate" in q):
            return {
                "type": "lead_conversion",
                "result": lead_conversion_rate(),
            }

        if "case" in q or "support" in q or "status" in q:
            return {
                "type": "cases_by_status",
                "result": open_cases_by_status().to_dict(orient="records"),
            }

        if "revenue" in q or "trend" in q or "monthly" in q:
            return {
                "type": "revenue_trend",
                "result": revenue_trend().to_dict(orient="records"),
            }

        if "top" in q and "opportunity" in q:
            return {
                "type": "top_opportunities",
                "result": top_opportunities_by_value().to_dict(orient="records"),
            }

        return {
            "type": "all_summary",
            "result": {
                "pipeline": pipeline_by_stage().to_dict(orient="records"),
                "lead_conversion": lead_conversion_rate(),
                "cases_by_status": open_cases_by_status().to_dict(orient="records"),
                "revenue_trend": revenue_trend().to_dict(orient="records"),
            },
        }

