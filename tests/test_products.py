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
        logger.info(f"Product: {data['data'].get('name')} successfully added and the product Id is {data.get('id')}")

    def test_add_product_with_missing_required_field(self, products_service):
        logger.info("TEST: Add product with missing required name field")
        result = products_service.addProduct({})
        assert result["status"] in (400, 422)

    @pytest.mark.skip(reason="ReqRes does not validate numeric fields")
    def test_add_product_with_invalid_price_or_stock(self, products_service):
        logger.info("TEST: Add product with invalid price and stock values")
        result = products_service.addProduct({
            "data": {
                "name": "Invalid Product",
                "price": "free",
                "stock": -10,
                "category": "Bath&Beauty",
                "image_url": "https://example.com/images/invalid-product.jpg",
                "description": "This product has invalid numeric fields"
            }
        })
        assert result["status"] in (400, 422)


class TestGetProducts:
    def test_get_all_products(self,products_service):
        logger.info("TEST: Get all Products")
        result = products_service.getProducts()
        assert result["status"] == 200
        data = result["body"]
        assert isinstance(data, (dict,list))
        logger.info(f"No of products available: {len(data['data'])}")
        
    def test_get_product_by_Id(self,products_service,create_product_id):
        logger.info("TEST: Get Product Byt Id")
        result = products_service.get_product_by_Id(create_product_id)
        assert result["status"] == 200
        data = result["body"]["data"]
        assert isinstance(data, (dict,list))
        assert data["id"] == create_product_id
        logger.info(f"Product Id: {data['id']} exists for {data['data']['name']}")
        
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
        logger.info("TEST: Update Product by Id")
        result = products_service.update_product_by_Id(create_product_id, {"data": {"stock": 210}})
        assert result["status"] == 200
        data = result["body"]
        assert data["data"]["stock"] == 210
        logger.info(f"Stock value: {data['data']['stock']} is updated for {create_product_id} at: {data['updatedAt']}")

    @pytest.mark.skip(reason="ReqRes does not validate id during update")
    def test_update_product_with_nonexistent_id(self, products_service):
        logger.info("TEST: Update product with non-existent id")
        result = products_service.update_product_by_Id("00000000-0000-0000-0000-000000000000", {"data": {"stock": 210}})
        assert result["status"] == 404
        
class TestDeleteProduct:
    def test_delete_products_by_id(self,products_service,create_product_id):
        logger.info(f"TEST: Delete product with product id")
        result = products_service.delete_product_by_Id(create_product_id)
        assert result["status"] == 204
        
    def test_delete_product_by_non_id_not_exist(self,products_service):
        logger.info(f"TEST: Delete product by giving non existant product id")
        result = products_service.delete_product_by_Id("8faafe85-70f2-47cc-8cb9-4a292a8af73a")
        assert result["status"] == 404
    def test_delete_product_with_invalid_id_format(self, products_service):
        logger.info("TEST: Delete product by invalid id format")
        result = products_service.delete_product_by_Id("invalid-product-id")
        assert result["status"] in (404, 500)

class TestApiStability:
    def _parse_json_body(self, response):
        try:
            return response.json()
        except ValueError:
            return None

    def test_invalid_resource_path_returns_404_or_500(self, products_service):
        logger.info("TEST: Invalid products endpoint should return a stable client error or server error")
        response = products_service.client.get("/api/collections/products/recordss")
        assert response.status_code in (404, 500)
        body = self._parse_json_body(response)
        assert body is None or isinstance(body, dict)

    def test_error_response_schema_for_invalid_product_id(self, products_service):
        logger.info("TEST: Error response schema is stable for invalid product id format")
        response = products_service.client.get("/api/collections/products/records/invalid-product-id")
        assert response.status_code in (404, 500)
        body = self._parse_json_body(response)
        assert isinstance(body, dict)
        assert any(key in body for key in ("error", "message", "status", "code"))