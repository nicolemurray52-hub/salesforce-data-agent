from __future__ import annotations

from simple_salesforce import Salesforce

from src.config import settings


class SalesforceClient:
    _client = None

    @classmethod
    def get_client(cls) -> Salesforce:
        if cls._client is None:
            if not all([settings.sf_username, settings.sf_password, settings.sf_security_token]):
                raise ValueError(
                    "Missing Salesforce credentials. Set SF_USERNAME, SF_PASSWORD, and SF_SECURITY_TOKEN in your environment."
                )

            domain = settings.sf_login_url.replace("https://", "").replace("http://", "").rstrip("/")
            cls._client = Salesforce(
                username=settings.sf_username,
                password=settings.sf_password,
                security_token=settings.sf_security_token,
                domain=domain,
            )

        return cls._client

    @staticmethod
    def query_all(soql: str):
        client = SalesforceClient.get_client()
        return client.query_all(soql)["records"]

    @staticmethod
    def get_opportunities():
        return SalesforceClient.query_all(
            """
            SELECT
                Id,
                Name,
                Amount,
                StageName,
                CloseDate,
                Owner.Name,
                Account.Name
            FROM Opportunity
            """
        )

    @staticmethod
    def get_leads():
        return SalesforceClient.query_all(
            """
            SELECT
                Id,
                Name,
                IsConverted,
                LeadSource,
                CreatedDate,
                ConvertedDate,
                Owner.Name
            FROM Lead
            """
        )

    @staticmethod
    def get_cases():
        return SalesforceClient.query_all(
            """
            SELECT
                Id,
                CaseNumber,
                Status,
                Priority,
                Origin,
                CreatedDate,
                Owner.Name
            FROM Case
            """
        )

