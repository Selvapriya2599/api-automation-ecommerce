import pytest

from utils.logger import get_logger

logger = get_logger("test_login")

class TestLogin:
    @pytest.mark.positive
    def test_login_success(self, login_page, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_page.login(valid_user["email"], valid_user["password"])

        assert result["status"] == 200
        assert "token" in result["body"]
        logger.info(f"Token: {result['body']['token']}")
        
    @pytest.mark.skip(reason="ReqRes does not validate passwords")
    def test_login_wrong_password(self, login_page, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_page.login(valid_user["email"], "wrong")

        assert result["status"] == 401
        assert "token" not in result["body"]
        
    @pytest.mark.negative
    def test_login_wrong_email(self, login_page, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_page.login("selva@gmail.com", valid_user["password"])

        assert result["status"] == 400
        assert "token" not in result["body"]
        
    @pytest.mark.negative
    def test_login_empty_email(self, login_page, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_page.login("", valid_user["password"])

        assert result["status"] == 400
        assert "token" not in result["body"]
        
    @pytest.mark.negative
    def test_login_empty_password(self, login_page, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_page.login(valid_user["email"],"")

        assert result["status"] == 400
        assert "token" not in result["body"]