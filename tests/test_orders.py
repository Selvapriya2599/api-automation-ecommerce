""" 
  Schema required
  customer_name   string   — name of the customer
  customer_email  email    — email of the customer
  product_ids     array    — list of product IDs in the order
  total_amount    number   — total order value
  order_date      date     — date order was placed (YYYY-MM-DD)
  status          string   — pending | shipped | delivered | cancelled
  """


import pytest
from utils.logger import get_logger

logger = get_logger("test_orders")

VALID_STATUSES = ["pending", "shipped", "delivered", "cancelled"]

class TestCreateOrders: 
    def test_create_successful_order(self,orders_page,orders_payload):
        logger.info("TEST: Creating a successful order")
        result = orders_page.create_successful_order(orders_payload)
        assert result["status"] in (200,201)
        data = result["body"]["data"]
        assert "id" in data.keys()
        assert "data" in data.keys()
        assert all(elem in data["data"] for elem in ["customer_name","customer_email","status","order_date","product_ids","total_amount"])
                
        assert data["data"] .get("customer_name") == orders_payload["data"]["customer_name"]
        assert data["data"] .get("customer_email") == orders_payload["data"]["customer_email"]
        assert data["data"] .get("status") == orders_payload["data"]["status"]
        assert data["data"] .get("order_date") == orders_payload["data"]["order_date"]
        assert data["data"] .get("product_ids") == orders_payload["data"]["product_ids"]
        assert data["data"] .get("total_amount") == orders_payload["data"]["total_amount"]
        logger.info(f"order successfully created for {data["data"].get("customer_name")} and the order id is {data.get("id")}")
    
    @pytest.mark.skip(reason="reqres is not validating the mandatory fieleds") 
    def test_create_order_with_missing_customerName(self,orders_page):
        logger.info("TEST: Creating order with missing customer name")
        result = orders_page.create_successful_order({
        "data": {
          "status": "pending",
           "order_date": "2026-03-20=1",
           "product_ids": [
              1,
              3
            ],
           "total_amount": 3571,
           "customer_name": "",
           "customer_email": "setup.user@example.com"
        }
        })
        assert result["status"] in (400,422)
        
class TestGetOrders:
    def test_get_orders(self,orders_page):
        logger.info(f"TEST: Get available orders")
        result = orders_page.get_orders()
        assert result["status"] == 200
        data = result["body"]
        assert isinstance(data, (dict,list))
        logger.info(f"No of orders received: {len(data["data"])}")
        for item in data["data"]:
            assert item["data"]["status"] in VALID_STATUSES
            logger.info(item["data"]["status"])
            
    def test_get_order_by_id(self,orders_page,create_order_id):
        logger.info(f"TEST: GET ORDER BY ORDER ID")
        result = orders_page.get_order_by_id(create_order_id)
        assert result["status"] == 200
        data = result["body"]["data"]
        assert data["id"] == create_order_id
        logger.info(f"Order Id: {data["id"] }exists for {data["data"]["customer_name"]} User")
        
    def test_get_order_with_non_existant_orderid(self,orders_page):
        logger.info(f"TEST: GET ORDER BY NON EXISTNAT ORDER ID")
        result = orders_page.get_order_by_id("8faafe85-70f2-47cc-8cb9-4a292a8af73a")
        assert result["status"] == 404
        
    def test_get_order_with_invalid_orderid(self,orders_page):
        logger.info(f"TEST: GET ORDER BY INVALID ORDER ID")
        result = orders_page.get_order_by_id("8faafe8570f2-73a")
        assert result["status"] == 500
           

class TestUpdateOrder:
            
    def test_update_order_by_id(self,orders_page,create_order_id):
        logger.info(f"TEST: Update order status delivered for the existing order")
        result = orders_page.update_order_by_id(create_order_id,{"data": {"status": "delivered"}})
        assert result["status"] == 200
        data = result["body"]
        assert data["data"]["status"] == "delivered"
        logger.info(f"Status: { data["data"]["status"]} and Updated at: {data["updatedAt"]}")
        
class TestDeleteOrder:
    def test_delete_order_by_id(self,orders_page,create_order_id):
        logger.info(f"TEST: Delete order with order id")
        result = orders_page.delete_order_by_id(create_order_id)
        assert result["status"] == 204
        
    def test_delete_order_by_wrong_non_existant_id(self,orders_page):
        logger.info(f"TEST: Delete order by giving non existant order id")
        result = orders_page.delete_order_by_id("8faafe85-70f2-47cc-8cb9-4a292a8af73a")
        assert result["status"] == 404
       
        
        
        
    
        
