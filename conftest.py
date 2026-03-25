import pytest

from pages.loginPage import LoginPage
from pages.ordersPage import OrdersPage
from utils.logger import get_logger

logger = get_logger("conftest")

@pytest.fixture(scope="session")
def login_page():
    return LoginPage()


@pytest.fixture(scope="session")
def orders_page():
    return OrdersPage()

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
def create_order_id(orders_page):
    logger.info("SETUP: CREATING A TEST PRODUCT")
    result = orders_page.create_successful_order({
     "data": {
          "status": "pending",
           "order_date": "2026-03-20=1",
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
    product_id = data["id"]
    logger.info(f"Test product created: {product_id}")
    return product_id

def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.passed:
            logger.info(f"PASSED  :: {report.nodeid}")
        elif report.failed:
            logger.error(f"FAILED  :: {report.nodeid}")
        elif report.skipped:
            logger.warning(f"SKIPPED :: {report.nodeid}")