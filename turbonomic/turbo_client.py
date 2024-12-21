import logging
import requests
import urllib3
import json

logger = logging.getLogger(__name__)
logging.captureWarnings(True)


class TurboClient:
    def __init__(self, base_url: str, user: str, password: str):
        self.base_url = f"https://{base_url}/api/v3"
        self.authentication = {'username': user, 'password': password}
        self.actions_filters = {
            "actionTypeList": [
                "START",
                "PROVISION",
                "ADD_PROVIDER",
                "BUY_RI",
                "TERMINATE",
                "SUSPEND",
                "DEACTIVATE"
            ],
            "relatedEntityTypes": [
                "PhysicalMachine"
            ],
            "detailLevel": "EXECUTION",
            "environmentType": "ONPREM"
            
        }
    
        #self.actions_filters = {'environmentType': 'ONPREM' }
        self.actions_filters2 = {
	"actionRelationTypeFilter": [
		"START",
		"PROVISION",
		"ADD_PROVIDER",
		"BUY_RI",
		"TERMINATE",
		"SUSPEND",
		"DEACTIVATE"
	],
	"environmentType": "ONPREM",
	"relatedEntityTypes": [
		"PhysicalMachine"
	]
}
        self.token = self.get_token()
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'cookie': self.token}

    @staticmethod
    def manage_resp(r):
        if r.status_code == 200:
            return r.json()
        else:
            logger.error(f"Error during the query, status code: {r.status_code}, with reason: {r.text}")
            return None

    def get_token(self):
        r = requests.post(f"{self.base_url}/login", data=self.authentication, verify=False)
        return r.headers['Set-Cookie'].split(';')[0]

    

    def list_machines_url(self, cursor: int = 0, limit: int = 0, is_physical=True, env: str = 'ONPREM'):
        machine_type = ("VirtualMachine", "PhysicalMachine", "ContainerPod")[is_physical]
        limit_url = (f"&limit={limit}", "")[limit == 0]
        cursor_url = (f"&cursor={cursor}", "")[cursor == 0]
        url = f"{self.base_url}/search?types={machine_type}&entity_types={machine_type}&environment_type={env}"
        url = f"{url}{cursor_url}{limit_url}&detail_type=entity&order_by=NAME&ascending=true"
        r = requests.get(url, headers=self.headers, verify=False)
        return self.manage_resp(r)

    def get_stats_by_uuid(self, uuid: str):
        url = f"{self.base_url}/stats/{uuid}"
        r = requests.get(url, headers=self.headers, verify=False)
        return self.manage_resp(r)

    def get_search_by_uuid(self, uuid: str):
        url = f"{self.base_url}/search/{uuid}"
        r = requests.get(url, headers=self.headers, verify=False)
        return self.manage_resp(r)

    def stats_url(self):
        return f"{self.base_url}/stats"
    
    def get_market_actions_by_uuid(self, uuid: str):
        print(self.actions_filters)
        url = f"{self.base_url}/markets/{uuid}/actions"
        r = requests.post(url, headers=self.headers, json=self.actions_filters, verify=False)
        return self.manage_resp(r)
