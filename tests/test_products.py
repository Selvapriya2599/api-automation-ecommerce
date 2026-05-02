import pytest
from utils.logger import get_logger

logger = get_logger("TestProducts")

class TestCreateProduct:
    def test_add_product(self,products_service,products_payload):
        logger.info("TEST: Add a new product to the catalogue")
        result = products_service.addProduct(products_payload)
        assert result["status"] in (200,201)
       
        data = result["body"]["data"]
        assert "id" in data.keys()
        assert "data" in data.keys()
        assert all(elem in data["data"].keys() for elem in ["name","price","stock","category","image_url","description"])
                
        assert data["data"] .get("name") == products_payload["data"]["name"]
        assert data["data"] .get("price") == products_payload["data"]["price"]
        assert data["data"] .get("stock") == products_payload["data"]["stock"]
        assert data["data"] .get("category") == products_payload["data"]["category"]
        assert data["data"] .get("image_url") == products_payload["data"]["image_url"]
        assert data["data"] .get("description") == products_payload["data"]["description"]
        logger.info(f"Prodct: {data["data"].get("name")} successfully added and the product Id is {data.get("id")}")
        
        

class TestGetProducts:
    def test_get_all_products(self,products_service):
        logger.info("TEST: Get all Products")
        result = products_service.getProducts()
        assert result["status"] == 200
        data = result["body"]
        assert isinstance(data, (dict,list))
        logger.info(f"No of products available: {len(data["data"])}")
        
    def test_get_product_by_Id(self,products_service,create_product_id):
        logger.info("TEST: Get Product Byt Id")
        result = products_service.get_product_by_Id(create_product_id)
        assert result["status"] == 200
        data = result["body"]["data"]
        assert isinstance(data, (dict,list))
        assert data["id"] == create_product_id
        logger.info(f"Product Id: {data["id"] }exists for {data["data"]["name"]}")
        
    def test_get_product_by_Id_not_exist(self,products_service):
        logger.info("TEST: Get Product Byt Id")
        result = products_service.get_product_by_Id("5f9cf9a5-621e-4ddb-ace1-09b008bee46d")
        assert result["status"] == 404
    
    def test_get_product_by_Id_wrong_format(self,products_service):
        logger.info("TEST: Get Product Byt Id")
        result = products_service.get_product_by_Id("5f9cf9a5621e4ddbace1")
        assert result["status"] in (404,500)
        
    
class TestUpdateProduct:
    def test_update_product_with_id(self,products_service,create_product_id):
        logger.info(f"TEST: Update Product by Id")
        result = products_service.update_product_by_Id(create_product_id, {"data": {"stock": 210}})
        assert result["status"] == 200
        data = result["body"]
        assert data["data"]["stock"] == 210
        logger.info(f"Stoclk value: { data["data"]["stock"]} is Updated for {create_product_id} at: {data["updatedAt"]}")
            
class TestDeleteProduct:
    def test_delete_products_by_id(self,products_service,create_product_id):
        logger.info(f"TEST: Delete product with product id")
        result = products_service.delete_product_by_Id(create_product_id)
        assert result["status"] == 204
        
    def test_delete_product_by_non_id_not_exist(self,products_service):
        logger.info(f"TEST: Delete product by giving non existant product id")
        result = products_service.delete_product_by_Id("8faafe85-70f2-47cc-8cb9-4a292a8af73a")
        assert result["status"] == 404 