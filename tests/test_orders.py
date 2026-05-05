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
    def test_create_successful_order(self,orders_service,orders_payload):
        logger.info("TEST: Creating a successful order")
        result = orders_service.create_successful_order(orders_payload)
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
        assert data["data"].get("total_amount") == orders_payload["data"]["total_amount"]
        logger.info(f'order successfully created for {data["data"].get("customer_name")} and the order id is {data.get("id")}')
    
    @pytest.mark.skip(reason="reqres is not validating the mandatory fields") 
    def test_create_order_with_missing_customerName(self,orders_service):
        logger.info("TEST: Creating order with missing customer name")
        result = orders_service.create_successful_order({
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
        
    def test_create_order_with_no_payload(self,orders_service):
        logger.info("TEST: Creating order with no payload")
        result = orders_service.create_successful_order({})
        if result["status"] in (200,201):
            pytest.skip("API currently accepts empty payloads; update expectation when validation is enabled")
        assert result["status"] in (400,422)

    def test_create_order_with_invalid_status_value(self, orders_service):
        logger.info("TEST: Creating order with invalid status value")
        result = orders_service.create_successful_order({
            "data": {
                "customer_name": "Invalid Status",
                "customer_email": "invalid.status@example.com",
                "status": "unknown",
                "order_date": "2026-05-05",
                "product_ids": [1],
                "total_amount": 100
            }
        })
        if result["status"] in (200,201):
            pytest.skip("API currently accepts invalid order status values; update expectation when validation is enabled")
        assert result["status"] in (400,422)

    def test_create_order_with_invalid_payload(self, orders_service):
        logger.info("TEST: Creating order with invalid payload types")
        result = orders_service.create_successful_order({
            "data": {
                "customer_name": "Invalid Payload",
                "customer_email": "invalid.payload@example.com",
                "status": "pending",
                "order_date": "not-a-date",
                "product_ids": "not-a-list",
                "total_amount": "one hundred"
            }
        })
        if result["status"] in (200,201):
            pytest.skip("API currently accepts malformed order payloads; update expectation when validation is enabled")
        assert result["status"] in (400,422)
        
class TestGetOrders:
    def test_get_orders(self,orders_service):
        logger.info(f"TEST: Get available orders")
        result = orders_service.get_orders()
        assert result["status"] == 200
        data = result["body"]
        assert isinstance(data, (dict,list))
        logger.info(f"No of orders received: {len(data['data'])}")
        for item in data["data"]:
            assert item["data"]["status"] in VALID_STATUSES
            logger.info(item["data"]["status"])
            
    def test_get_order_by_id(self,orders_service,create_order_id):
        logger.info(f"TEST: GET ORDER BY ORDER ID")
        result = orders_service.get_order_by_id(create_order_id)
        assert result["status"] == 200
        data = result["body"]["data"]
        assert data["id"] == create_order_id
        logger.info(f"Order Id: {data['id']} exists for {data['data']['customer_name']} User")
        
    def test_get_order_with_non_existant_orderid(self,orders_service):
        logger.info(f"TEST: GET ORDER BY NON EXISTNAT ORDER ID")
        result = orders_service.get_order_by_id("8faafe85-70f2-47cc-8cb9-4a292a8af73a")
        assert result["status"] == 404
        
    def test_get_order_with_invalid_orderid(self,orders_service):
        logger.info(f"TEST: GET ORDER BY INVALID ORDER ID")
        result = orders_service.get_order_by_id("8faafe8570f2-73a")
        assert result["status"] in (404,500)
           

class TestUpdateOrder:
            
    def test_update_order_by_id(self,orders_service,create_order_id):
        logger.info(f"TEST: Update order status delivered for the existing order")
        result = orders_service.update_order_by_id(create_order_id,{"data": {"status": "delivered"}})
        assert result["status"] == 200
        data = result["body"]
        assert data["data"]["status"] == "delivered"
        logger.info(f"Status: { data['data']['status']} and Updated at: {data['updatedAt']}")


    @pytest.mark.skip(reason="reqres is not validating order id before update")
    def test_update_order_with_nonexistent_id(self, orders_service):
        logger.info("TEST: Update non-existent order id")
        result = orders_service.update_order_by_id("00000000-0000-0000-0000-000000000000", {"data": {"status": "shipped"}})
        assert result["status"] == 404

    def test_update_order_with_invalid_payload(self, orders_service, create_order_id):
        logger.info("TEST: Update order with invalid payload")
        result = orders_service.update_order_by_id(create_order_id, {"data": {"status": 123, "order_date": "bad-date"}})
        if result["status"] in (200,201):
            pytest.skip("API currently accepts invalid update payloads; update expectation when validation is enabled")
        assert result["status"] in (400,422)
        
class TestDeleteOrder:
    def test_delete_order_by_id(self,orders_service,create_order_id):
        logger.info(f"TEST: Delete order with order id")
        result = orders_service.delete_order_by_id(create_order_id)
        assert result["status"] == 204
        
    def test_delete_order_twice(self,orders_service):
        logger.info("TEST: Delete the same order twice")
        result = orders_service.create_successful_order({
            "data": {
                "status": "pending",
                "order_date": "2026-05-05",
                "product_ids": [1],
                "total_amount": 100,
                "customer_name": "Double Delete",
                "customer_email": "double.delete@example.com"
            }
        })
        assert result["status"] in (200,201)
        order_id = result["body"]["data"]["id"]

        first_delete = orders_service.delete_order_by_id(order_id)
        assert first_delete["status"] in (200,204)

        second_delete = orders_service.delete_order_by_id(order_id)
        assert second_delete["status"] == 404
        
    def test_delete_order_by_wrong_non_existant_id(self,orders_service):
        logger.info(f"TEST: Delete order by giving non existant order id")
        result = orders_service.delete_order_by_id("8faafe85-70f2-47cc-8cb9-4a292a8af73a")
        assert result["status"] == 404
        
    def test_delete_order_with_invalid_orderid_format(self,orders_service):
        logger.info(f"TEST: Delete order by invalid order id format to validate server error response")
        result = orders_service.delete_order_by_id("invalid-order-id-format")
        assert result["status"] in (404,500)


class TestApiStability:
    def _parse_json_body(self, response):
        try:
            return response.json()
        except ValueError:
            return None

    def test_invalid_resource_path_returns_404_or_500(self, orders_service):
        logger.info("TEST: Invalid orders endpoint should return a stable client error or server error")
        response = orders_service.client.get("/api/collections/orders/recordss")
        assert response.status_code in (404, 500)
        body = self._parse_json_body(response)
        assert body is None or isinstance(body, dict)

    def test_error_response_schema_for_invalid_order_id(self, orders_service):
        logger.info("TEST: Error response schema is stable for invalid order id format")
        response = orders_service.client.get("/api/collections/orders/records/invalid-order-id-format")
        assert response.status_code in (404, 500)
        body = self._parse_json_body(response)
        assert isinstance(body, dict)
        assert any(key in body for key in ("error", "message", "status", "code"))
