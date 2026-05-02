from utils.api_client import APIClient
from utils.logger import get_logger


logger = get_logger("OrdersPage")
EndPoint = "/api/collections/orders/records"

class OrdersService:
    def __init__(self):
        self.client = APIClient()
        
    def get_orders(self) -> dict:
        logger.info(f"Getting order details")
        res = self.client.get(EndPoint)
        return {"status": res.status_code, "body": res.json()}
    
    def create_successful_order(self,payload:dict) -> dict:
        logger.info(f"Creating successful order for: {payload}")
        res = self.client.post(EndPoint,payload)
        return {"status":res.status_code, "body":res.json()}
    
    def get_order_by_id(self,id:str) -> dict:
        logger.info(f"Getting order details for id {id}")
        res = self.client.get(f"{EndPoint}/{id}")
        return{"status":res.status_code, "body":res.json()}
    
    def update_order_by_id(self,id:str,payload:dict) -> dict:
        logger.info(f"Updating status of order with id {id} to delivered")
        res = self.client.patch(f"{EndPoint}/{id}",payload)
        return{"status":res.status_code, "body":res.json()}
    
    def delete_order_by_id(self,id:str) -> dict:
        logger.info(f"Deleting order with ID: {id}")
        res = self.client.delete(f"{EndPoint}/{id}")
        return {"status":res.status_code}
    