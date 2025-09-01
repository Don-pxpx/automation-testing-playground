"""
Base API Client for Automation Testing Playground
Provides common functionality for API testing including request methods, 
response validation, and error handling
"""

import requests
import json
import time
from typing import Dict, Any, Optional, Union
from jsonschema import validate, ValidationError
from jsonpath_ng import parse
from helpers.log_helpers import InlineLogger
from config.api_config import APIConfig


class BaseAPIClient:
    """Base API client with common functionality for all API testing"""
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL for the API
            headers: Optional custom headers
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {**APIConfig.DEFAULT_HEADERS, **(headers or {})}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger = InlineLogger()
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request with retry logic and logging
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response object
        """
        url = f"{self.base_url}{endpoint}"
        
        # Set default timeout if not provided
        if 'timeout' not in kwargs:
            kwargs['timeout'] = APIConfig.REQUEST_TIMEOUT
            
        self.logger.step(f"Making {method.upper()} request to {url}")
        
        # Retry logic
        for attempt in range(APIConfig.MAX_RETRIES):
            try:
                response = self.session.request(method, url, **kwargs)
                self.logger.success(f"Request successful (Status: {response.status_code})")
                return response
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
                if attempt < APIConfig.MAX_RETRIES - 1:
                    time.sleep(APIConfig.RETRY_DELAY)
                else:
                    self.logger.error(f"All {APIConfig.MAX_RETRIES} attempts failed")
                    raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a GET request"""
        return self._make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make a POST request"""
        if data:
            kwargs['json'] = data
        return self._make_request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make a PUT request"""
        if data:
            kwargs['json'] = data
        return self._make_request('PUT', endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make a PATCH request"""
        if data:
            kwargs['json'] = data
        return self._make_request('PATCH', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a DELETE request"""
        return self._make_request('DELETE', endpoint, **kwargs)
    
    def verify_status_code(self, response: requests.Response, expected_status: Union[int, list]) -> bool:
        """
        Verify that the response status code matches expected value(s)
        
        Args:
            response: Response object to verify
            expected_status: Expected status code(s) - can be int or list of ints
            
        Returns:
            bool: True if status code matches, False otherwise
        """
        if isinstance(expected_status, int):
            expected_status = [expected_status]
            
        if response.status_code in expected_status:
            self.logger.success(f"Status code {response.status_code} matches expected: {expected_status}")
            return True
        else:
            self.logger.error(f"Status code {response.status_code} does not match expected: {expected_status}")
            return False
    
    def verify_response_time(self, response: requests.Response, max_time: float = 5.0) -> bool:
        """
        Verify that the response time is within acceptable limits
        
        Args:
            response: Response object to verify
            max_time: Maximum acceptable response time in seconds
            
        Returns:
            bool: True if response time is acceptable, False otherwise
        """
        response_time = response.elapsed.total_seconds()
        
        if response_time <= max_time:
            self.logger.success(f"Response time {response_time:.2f}s is within limit ({max_time}s)")
            return True
        else:
            self.logger.warning(f"Response time {response_time:.2f}s exceeds limit ({max_time}s)")
            return False
    
    def verify_json_schema(self, response: requests.Response, schema: Dict[str, Any]) -> bool:
        """
        Verify that the response JSON matches the expected schema
        
        Args:
            response: Response object to verify
            schema: JSON schema to validate against
            
        Returns:
            bool: True if schema validation passes, False otherwise
        """
        try:
            response_json = response.json()
            validate(instance=response_json, schema=schema)
            self.logger.success("JSON schema validation passed")
            return True
        except ValidationError as e:
            self.logger.error(f"JSON schema validation failed: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            return False
    
    def extract_value_by_jsonpath(self, response: requests.Response, jsonpath: str) -> Any:
        """
        Extract a value from the response using JSONPath
        
        Args:
            response: Response object
            jsonpath: JSONPath expression
            
        Returns:
            Extracted value or None if not found
        """
        try:
            response_json = response.json()
            jsonpath_expr = parse(jsonpath)
            matches = [match.value for match in jsonpath_expr.find(response_json)]
            
            if matches:
                self.logger.note(f"Extracted value using JSONPath '{jsonpath}': {matches[0]}")
                return matches[0] if len(matches) == 1 else matches
            else:
                self.logger.warning(f"No matches found for JSONPath: {jsonpath}")
                return None
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            return None
    
    def verify_response_contains(self, response: requests.Response, expected_content: Dict[str, Any]) -> bool:
        """
        Verify that the response contains expected content
        
        Args:
            response: Response object to verify
            expected_content: Dictionary of expected key-value pairs
            
        Returns:
            bool: True if all expected content is found, False otherwise
        """
        try:
            response_json = response.json()
            
            for key, expected_value in expected_content.items():
                if key not in response_json:
                    self.logger.error(f"Key '{key}' not found in response")
                    return False
                    
                actual_value = response_json[key]
                if actual_value != expected_value:
                    self.logger.error(f"Value mismatch for key '{key}': expected {expected_value}, got {actual_value}")
                    return False
            
            self.logger.success("All expected content found in response")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            return False
    
    def log_response_details(self, response: requests.Response) -> None:
        """
        Log detailed information about the response
        
        Args:
            response: Response object to log
        """
        self.logger.note(f"Response Status: {response.status_code}")
        self.logger.note(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        self.logger.note(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            self.logger.note(f"Response Body: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            self.logger.note(f"Response Body: {response.text}")
