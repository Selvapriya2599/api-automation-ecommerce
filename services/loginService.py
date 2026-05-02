from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger("LoginPage")

class LoginService:
    def __init__(self):
        self.client = APIClient()
        
    def login(self,email:str, password:str) -> dict :
        logger.info(f"Logging in {email}")
        res = self.client.post("/api/login", {"email": email, "password": password})
        return {"status": res.status_code, "body": res.json()}