import requests

class SonarClient:
    def __init__(self, url, project_key, auth):
        self.url = url
        self.project_key = project_key
        res = requests.post(f"{self.url}/api/authentication/login", data=auth)
        self.cookies = {"JWT-SESSION": res.cookies.get_dict().get("JWT-SESSION")}

    def construct_endpoint(self, rule_key: str) -> str:
        return f"{self.url}/api/issues/search?rules={rule_key}&resolved=no&componentKeys={self.project_key}"

    def query(self, rule_key: str) -> int:
        endpoint = self.construct_endpoint(rule_key)
        data = requests.get(endpoint, cookies=self.cookies)
        return data.json()["total"]