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
    
    def get(self,endpoint: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET Request {url}  & params={params}")
        res = self.session.get(url,headers=self._header(),params=params)
        logger.debug(f" {res.status_code}: {res.text[:300]}")
        return res
    
    def post(self,endpoint:str,payload:dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST Request {url}  & payload={payload}")
        res = self.session.post(url,headers=self._header(use_manage=True),json=payload)
        logger.debug(f" {res.status_code}: {res.text[:300]}")
        return res
    
    def patch(self,endpoint:str,payload:dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Patch Request {url}  & payload={payload}")
        res = self.session.patch(url,headers=self._header(use_manage=True),json=payload)
        logger.debug(f" {res.status_code}: {res.text[:300]}")
        return res
    
    def delete(self,endpoint:str) -> requests.Response :
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE Request {url}")
        res = self.session.delete(url, headers=self._header(use_manage=True))
        logger.debug(f" {res.status_code}: {res.text[:300]}")
        return res