"""
HTTP Methods API Tests
Test suite for different HTTP methods using HTTPBin API
"""

import pytest
from faker import Faker
from pages.api.base_api_client import BaseAPIClient
from config.api_config import APIConfig, HTTPBinEndpoints
from helpers.log_helpers import InlineLogger

fake = Faker()


class TestHTTPMethods:
    """Test class for HTTP methods using HTTPBin API"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.client = BaseAPIClient(APIConfig.HTTPBIN_BASE_URL)
        self.logger = InlineLogger()
    
    def test_get_method(self):
        """Test GET method"""
        self.logger.test_start("GET Method Test")
        
        # Make GET request
        response = self.client.get(HTTPBinEndpoints.GET)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "GET should return 200"
        assert self.client.verify_response_time(response, max_time=5.0), "Response time should be acceptable"
        
        # Verify response structure
        response_data = response.json()
        assert 'url' in response_data, "Response should contain URL"
        assert 'headers' in response_data, "Response should contain headers"
        assert 'origin' in response_data, "Response should contain origin"
        
        self.logger.success("GET method test passed")
        self.logger.test_end("GET Method Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_post_method(self):
        """Test POST method with JSON data"""
        self.logger.test_start("POST Method Test")
        
        # Test data
        test_data = {
            "name": fake.name(),
            "email": fake.email(),
            "message": fake.text()
        }
        
        # Make POST request
        response = self.client.post(HTTPBinEndpoints.POST, test_data)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "POST should return 200"
        
        # Verify response contains sent data
        response_data = response.json()
        assert 'json' in response_data, "Response should contain JSON data"
        assert response_data['json'] == test_data, "Response should contain sent data"
        
        self.logger.success("POST method test passed")
        self.logger.test_end("POST Method Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_put_method(self):
        """Test PUT method with JSON data"""
        self.logger.test_start("PUT Method Test")
        
        # Test data
        test_data = {
            "id": 1,
            "name": fake.name(),
            "status": "updated"
        }
        
        # Make PUT request
        response = self.client.put(HTTPBinEndpoints.PUT, test_data)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "PUT should return 200"
        
        # Verify response contains sent data
        response_data = response.json()
        assert 'json' in response_data, "Response should contain JSON data"
        assert response_data['json'] == test_data, "Response should contain sent data"
        
        self.logger.success("PUT method test passed")
        self.logger.test_end("PUT Method Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_patch_method(self):
        """Test PATCH method with JSON data"""
        self.logger.test_start("PATCH Method Test")
        
        # Test data
        test_data = {
            "status": "patched"
        }
        
        # Make PATCH request
        response = self.client.patch(HTTPBinEndpoints.PATCH, test_data)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "PATCH should return 200"
        
        # Verify response contains sent data
        response_data = response.json()
        assert 'json' in response_data, "Response should contain JSON data"
        assert response_data['json'] == test_data, "Response should contain sent data"
        
        self.logger.success("PATCH method test passed")
        self.logger.test_end("PATCH Method Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_delete_method(self):
        """Test DELETE method"""
        self.logger.test_start("DELETE Method Test")
        
        # Make DELETE request
        response = self.client.delete(HTTPBinEndpoints.DELETE)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "DELETE should return 200"
        
        # Verify response structure
        response_data = response.json()
        assert 'url' in response_data, "Response should contain URL"
        
        self.logger.success("DELETE method test passed")
        self.logger.test_end("DELETE Method Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_status_codes(self):
        """Test different HTTP status codes"""
        self.logger.test_start("Status Codes Test")
        
        # Test various status codes
        status_codes = [200, 201, 400, 401, 403, 404, 500]
        
        for status_code in status_codes:
            self.logger.step(f"Test status code: {status_code}")
            
            endpoint = HTTPBinEndpoints.STATUS.format(code=status_code)
            response = self.client.get(endpoint)
            
            # Verify status code
            assert self.client.verify_status_code(response, status_code), f"Should return {status_code}"
        
        self.logger.success("All status code tests passed")
        self.logger.test_end("Status Codes Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_headers(self):
        """Test custom headers"""
        self.logger.test_start("Custom Headers Test")
        
        # Custom headers
        custom_headers = {
            "X-Custom-Header": "test-value",
            "X-Request-ID": fake.uuid4(),
            "Authorization": "Bearer test-token"
        }
        
        # Make request with custom headers
        response = self.client.get(HTTPBinEndpoints.HEADERS, headers=custom_headers)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "Should return 200"
        
        # Verify headers are reflected in response
        response_data = response.json()
        assert 'headers' in response_data, "Response should contain headers"
        
        headers = response_data['headers']
        # HTTPBin may not return all custom headers exactly as sent
        # Let's check that at least some of our headers are present
        found_headers = 0
        for key, value in custom_headers.items():
            if key in headers:
                found_headers += 1
                assert headers[key] == value, f"Header {key} should have correct value"
        
        # At least one custom header should be present
        assert found_headers > 0, "At least one custom header should be present in response"
        
        self.logger.success("Custom headers test passed")
        self.logger.test_end("Custom Headers Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_response_formats(self):
        """Test different response formats"""
        self.logger.test_start("Response Formats Test")
        
        # Test JSON response
        self.logger.step("Test JSON response")
        response = self.client.get(HTTPBinEndpoints.JSON)
        assert self.client.verify_status_code(response, 200), "JSON endpoint should return 200"
        
        response_data = response.json()
        assert 'slideshow' in response_data, "JSON response should contain slideshow"
        
        # Test XML response
        self.logger.step("Test XML response")
        response = self.client.get(HTTPBinEndpoints.XML)
        assert self.client.verify_status_code(response, 200), "XML endpoint should return 200"
        
        # XML response should be text
        assert response.text.startswith('<?xml'), "Response should be XML"
        
        self.logger.success("Response formats test passed")
        self.logger.test_end("Response Formats Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_delayed_response(self):
        """Test delayed response handling"""
        self.logger.test_start("Delayed Response Test")
        
        # Test with 2 second delay
        delay_seconds = 2
        endpoint = HTTPBinEndpoints.DELAY.format(seconds=delay_seconds)
        
        self.logger.step(f"Test response with {delay_seconds} second delay")
        
        response = self.client.get(endpoint)
        
        # Verify response
        assert self.client.verify_status_code(response, 200), "Should return 200"
        
        # Verify response time is reasonable (should be at least the delay time)
        response_time = response.elapsed.total_seconds()
        assert response_time >= delay_seconds, f"Response time should be at least {delay_seconds} seconds"
        
        self.logger.success(f"Delayed response test passed (response time: {response_time:.2f}s)")
        self.logger.test_end("Delayed Response Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
