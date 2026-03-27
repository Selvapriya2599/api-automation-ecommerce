from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger("ProductsPage")

Endpoint = "/api/collections/products/records"
class ProductsPage:
    def __init__(self):
        self.client = APIClient()
        
    def getProducts(self) -> dict:
        logger.info(f"Getting all the available products in {Endpoint}")
        res = self.client.get(Endpoint)
        return {"status": res.status_code, "body":res.json()}
    
    def addProduct(self,payload:dict) -> dict:
        logger.info(f"Creating a new product for json: {payload}")
        res = self.client.post(Endpoint,payload)
        return {"status": res.status_code, "body":res.json()}
    
    def get_product_by_Id(self,productId:str) -> dict:
        logger.info(f"Get product for the given Id {productId}")
        res = self.client.get(f"{Endpoint}/{productId}")
        return {"status": res.status_code, "body":res.json()}
    
    def update_product_by_Id(self,productId:str,payload:dict) -> dict:
        logger.info(f"Update product's stock value for the given Id {productId}")
        res = self.client.patch(f"{Endpoint}/{productId}",payload)
        return {"status": res.status_code, "body":res.json()}
    
    def delete_product_by_Id(self,productId:str) -> dict:
        logger.info(f"Delete product for the given Id {productId}")
        res = self.client.delete(f"{Endpoint}/{productId}")
        return {"status": res.status_code}