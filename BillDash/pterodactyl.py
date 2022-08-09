import json
import requests


class Pterodactyl:
    def __init__(self, api_key, api_endpoint):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_server_info(self, server_id: int) -> dict:
        url = f"{self.api_endpoint}/api/application/server/{server_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_new_user(
        self, email: str, username: str, first_name: str, last_name: str
    ) -> dict:
        url = f"{self.api_endpoint}/api/application/users"
        payload = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if not resp.status_code == 201:
            print(resp.text, resp.status_code)
            return None
        return resp.json()

    def delete_user(self, id: int) -> bool:
        url = f"{self.api_endpoint}/api/application/users/{id}"
        resp = requests.delete(url, headers=self.headers)
        if resp.status_code == 204:
            return True
        return False

    def get_egg_info(self, nest_id, egg_id):
        url = f"{self.api_endpoint}/api/application/nests/{nest_id}/eggs/{egg_id}?include=variables,config"
        resp = requests.get(url, headers=self.headers)
        if not resp.status_code == 200:
            return None
        return resp.json()

    def create_new_server(
        self,
        name: str,
        user: int,
        egg: int,
        docker_image: str,
        startup: str,
        environment: dict,
        limits: dict,
        feature_limits: dict,
        location: list,
        dedicated_ip: bool,
    ):
        server_specs = {
            "name": name,
            "user": user,
            "egg": egg,
            "docker_image": docker_image,
            "startup": startup,
            "environment": environment,
            "limits": limits,
            "feature_limits": feature_limits,
            "deploy": {
                "locations": location,
                "dedicated_ip": dedicated_ip,
                "port_range": [],
            },
        }
        payload = json.dumps(server_specs)
        url = f"{self.api_endpoint}/api/application/servers"
        resp = requests.post(url, headers=self.headers, data=payload)
        if not resp.status_code == 201:
            return None
        return resp.json()

    def delete_server(self, server_id: int) -> bool:
        url = f"{self.api_endpoint}/api/application/servers/{server_id}"
        resp = requests.delete(url, headers=self.headers)
        if resp.status_code == 204:
            return True
        return False
