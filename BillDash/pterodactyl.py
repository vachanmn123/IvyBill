from urllib import response
import requests


class Pterodactyl:
    def __init__(self, api_key, api_endpoint):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def get_server_info(self, server_id: int) -> dict:
        url = f"{self.api_endpoint}/api/application/server/{server_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json()
