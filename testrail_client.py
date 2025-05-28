import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

class TestRailClient:
    def __init__(self):
        self.base_url = os.getenv('TESTRAIL_BASE_URL')
        self.user = os.getenv('TESTRAIL_USER')
        self.api_key = os.getenv('TESTRAIL_API_KEY')
        self.auth = HTTPBasicAuth(self.user, self.api_key)
        self.headers = {'Content-Type': 'application/json'}

    def _url(self, endpoint):
        return f"{self.base_url}/index.php?/api/v2/{endpoint}"

    def get_projects(self):
        url = self._url("get_projects")
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def add_test_run(self, project_id, suite_id, name, description=""):
        url = self._url("add_run/" + str(project_id))
        payload = {
            "suite_id": suite_id,
            "name": name,
            "description": description,
            "include_all": True
        }
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def add_test_result(self, test_id, status_id, comment=""):
        url = self._url("add_result/" + str(test_id))
        payload = {
            "status_id": status_id,
            "comment": comment
        }
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
