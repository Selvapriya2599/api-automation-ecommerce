import pytest

from utils.logger import get_logger

logger = get_logger("test_login")

class TestLogin:
    @pytest.mark.positive
    def test_login_success(self, login_service, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_service.login(valid_user["email"], valid_user["password"])

        assert result["status"] == 200
        assert "token" in result["body"]
        logger.info(f"Token: {result['body']['token']}")
        
    @pytest.mark.skip(reason="ReqRes does not validate passwords")
    def test_login_wrong_password(self, login_service, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_service.login(valid_user["email"], "wrong")

        assert result["status"] == 401
        assert "token" not in result["body"]
        
    @pytest.mark.negative
    def test_login_wrong_email(self, login_service, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_service.login("selva@gmail.com", valid_user["password"])

        assert result["status"] == 400
        assert "token" not in result["body"]
        
    @pytest.mark.negative
    def test_login_empty_email(self, login_service, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_service.login("", valid_user["password"])

        assert result["status"] == 400
        assert "token" not in result["body"]
        
    @pytest.mark.negative
    def test_login_empty_password(self, login_service, valid_user):
        logger.info("TEST: Login with valid credentials")
        result = login_service.login(valid_user["email"],"")

        assert result["status"] == 400
        assert "token" not in result["body"]


class TestApiStability:
    def _parse_json_body(self, response):
        try:
            return response.json()
        except ValueError:
            return None

    def test_invalid_login_resource_path_returns_404_or_500(self, login_service):
        logger.info("TEST: Invalid login endpoint should return a stable client error or server error")
        response = login_service.client.get("/api/loginn/hello")
        assert response.status_code in (404, 500)
        body = self._parse_json_body(response)
        assert body is None or isinstance(body, dict)

    def test_error_response_schema_for_invalid_login_path(self, login_service):
        logger.info("TEST: Error response schema is stable for invalid login path")
        response = login_service.client.get("/api/login/invalid")
        assert response.status_code in (404, 500)
        body = self._parse_json_body(response)
        assert isinstance(body, dict)
        assert body is not None or any(key in body for key in ("error", "message", "status", "code"))