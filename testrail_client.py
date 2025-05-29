import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TestRailClient:
    def __init__(self):
        self.base_url = os.getenv("TESTRAIL_BASE_URL")
        self.username = os.getenv("TESTRAIL_USERNAME")
        self.api_key = os.getenv("TESTRAIL_API_KEY")

        if not all([self.base_url, self.username, self.api_key]):
            raise ValueError("Missing TestRail credentials in .env file")

        self.base_url = self.base_url.rstrip("/")
        self.auth = (self.username, self.api_key)
        self.headers = {"Content-Type": "application/json"}

    def get_tests(self, run_id):
        url = f"{self.base_url}/index.php?/api/v2/get_tests/{run_id}"
        print(f"Fetching TestRail data from: {url}")

        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
