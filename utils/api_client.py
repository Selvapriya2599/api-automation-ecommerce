import requests
from config import BASE_URL,PUBLIC_KEY,MANAGE_KEY
from utils.logger import get_logger

logger = get_logger("api_client")

class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        
    def _header(self,use_manage=False) -> dict:
        key = MANAGE_KEY if use_manage else PUBLIC_KEY
        
        return {"x-api-key":key,"Content-Type": "application/json"}
    
    def request(self, method: str, endpoint: str,use_manage: bool = False,**kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"{method.upper()} {url} | kwargs={kwargs}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self._header(use_manage),
                timeout=10,       
                **kwargs
            )
            logger.debug(f"{response.status_code}: {response.text[:300]}")
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get(self,endpoint: str, params: dict = None) -> requests.Response:
        return self.request("get", endpoint, params=params)
    
    def post(self, endpoint: str, payload: dict) -> requests.Response:
        return self.request("post", endpoint, json=payload, use_manage=True)

    def patch(self, endpoint: str, payload: dict) -> requests.Response:
        return self.request("patch", endpoint, json=payload, use_manage=True)

    def delete(self, endpoint: str) -> requests.Response:
        return self.request("delete", endpoint, use_manage=True)