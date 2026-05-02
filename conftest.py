import pytest

from services.loginService import LoginService
from services.ordersService import OrdersService
from services.productsService import ProductsService
from utils.logger import get_logger

logger = get_logger("conftest")

@pytest.fixture(scope="session")
def login_service():
    return LoginService()


@pytest.fixture(scope="session")
def orders_service():
    return OrdersService()

@pytest.fixture(scope="session")
def products_service():
    return ProductsService()

@pytest.fixture(scope="session")
def valid_user():
    return {"email": "eve.holt@reqres.in", "password": "cityslicka"}

@pytest.fixture(scope="class")
def orders_payload():
    return {
     "data": {
          "status": "delivered",
           "order_date": "2026-03-20",
           "product_ids": [
              3,
              5
            ],
           "total_amount": 3998,
          "customer_name": "Shankar Raja",
           "customer_email": "shankar.raja@example.com"
        }
    }

@pytest.fixture(scope="class")
def products_payload():
    return {
      "data": {
      "name": "CeraVe BodyLotion",
      "price": 2000,
      "stock": 200,
      "category": "Bath&Beauty",
      "image_url": "https://example.com/images/creave-lotion.jpg",
      "description": "Creave Body Lotion with Ceramide and Chia butter for Dry to Extreme Dry skin"
    }}
    
@pytest.fixture(scope="class")
def create_order_id(orders_service):
    logger.info("SETUP: CREATING A TEST ORDER")
    result = orders_service.create_successful_order({
     "data": {
          "status": "pending",
           "order_date": "2026-03-20-1",
           "product_ids": [
              1,
              3
            ],
           "total_amount": 3571,
           "customer_name": "Setup User",
           "customer_email": "setup.user@example.com"
        }
    })
    assert result["status"] in (200,201)
    data = result["body"]["data"]
    assert "id" in data.keys()
    order_id = data["id"]
    logger.info(f"Test product created: {order_id}")    
    yield order_id
    
    logger.info(f"TEARDOWN: DELETING ORDER {order_id}")
    delete_res = orders_service.delete_order_by_id(order_id)
    assert delete_res["status"] in (200, 204)

@pytest.fixture(scope="class")
def create_product_id(products_service):
    logger.info("SETUP: CREATING A TEST PRODUCT")
    result = products_service.addProduct({
     "data": {
      "name": "Test Prodcut",
      "price": 2000,
      "stock": 210,
      "category": "Bath&Beauty",
      "image_url": "https://example.com/images/test-product.jpg",
      "description": "This is a test product"
        }
    })
    assert result["status"] in (200,201)
    data = result["body"]["data"]
    assert "id" in data.keys()
    product_id = data["id"]
    logger.info(f"Test product created: {product_id}")
    yield product_id
    
    logger.info(f"TEARDOWN: DELETING PRODUCT {product_id}")
    delete_res = products_service.delete_product_by_Id(product_id)
    assert delete_res["status"] in (200, 204)


def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.passed:
            logger.info(f"PASSED  :: {report.nodeid}")
        elif report.failed:
            logger.error(f"FAILED  :: {report.nodeid}")
        elif report.skipped:
            logger.warning(f"SKIPPED :: {report.nodeid}")
            