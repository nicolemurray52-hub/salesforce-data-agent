import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.sf_username = os.getenv("SF_USERNAME")
        self.sf_password = os.getenv("SF_PASSWORD")
        self.sf_security_token = os.getenv("SF_SECURITY_TOKEN")
        self.sf_login_url = os.getenv("SF_LOGIN_URL", "https://login.salesforce.com")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")


settings = Settings()

