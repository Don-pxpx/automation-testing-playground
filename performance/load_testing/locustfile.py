"""
Locust load testing configuration for Performance & Security Testing Lab
Provides comprehensive load testing scenarios for web applications
"""

import time
import random
from typing import Dict, Any
from locust import HttpUser, task, between, events
from locust.exception import StopUser

from helpers.logger import PerformanceSecurityLogger

# Initialize logger
logger = PerformanceSecurityLogger("LocustLoadTest")


class WebAppUser(HttpUser):
    """
    Simulates a user browsing a web application
    Includes realistic user behavior patterns
    """
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        logger.info(f"User {self.client.base_url} started browsing")
    
    def on_stop(self):
        """Called when a user stops"""
        logger.info(f"User {self.client.base_url} finished browsing")
    
    @task(3)
    def view_homepage(self):
        """View the homepage - high frequency task"""
        with logger.performance_context("Homepage Load"):
            response = self.client.get("/")
            
            if response.status_code == 200:
                logger.success("Homepage loaded successfully")
                logger.performance_metric("Homepage Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Homepage failed with status {response.status_code}")
    
    @task(2)
    def browse_products(self):
        """Browse product listings - medium frequency task"""
        with logger.performance_context("Product Browse"):
            # Simulate browsing different product categories
            categories = ["electronics", "clothing", "books", "home"]
            category = random.choice(categories)
            
            response = self.client.get(f"/products/{category}")
            
            if response.status_code == 200:
                logger.success(f"Product category {category} loaded successfully")
                logger.performance_metric("Product Browse Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Product browse failed with status {response.status_code}")
    
    @task(1)
    def view_product_details(self):
        """View specific product details - low frequency task"""
        with logger.performance_context("Product Details"):
            # Simulate viewing a specific product
            product_id = random.randint(1, 100)
            
            response = self.client.get(f"/product/{product_id}")
            
            if response.status_code == 200:
                logger.success(f"Product {product_id} details loaded successfully")
                logger.performance_metric("Product Details Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Product details failed with status {response.status_code}")
    
    @task(1)
    def search_products(self):
        """Search for products - low frequency task"""
        with logger.performance_context("Product Search"):
            # Simulate search queries
            search_terms = ["laptop", "phone", "shirt", "book", "tablet"]
            search_term = random.choice(search_terms)
            
            response = self.client.get(f"/search?q={search_term}")
            
            if response.status_code == 200:
                logger.success(f"Search for '{search_term}' completed successfully")
                logger.performance_metric("Search Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Search failed with status {response.status_code}")


class APILoadUser(HttpUser):
    """
    Simulates API usage patterns
    Tests REST API endpoints under load
    """
    
    wait_time = between(0.5, 2)  # Faster API calls
    
    def on_start(self):
        """Called when a user starts"""
        logger.info(f"API User {self.client.base_url} started")
    
    @task(4)
    def get_data(self):
        """GET request - high frequency"""
        with logger.performance_context("API GET Request"):
            response = self.client.get("/api/data")
            
            if response.status_code == 200:
                logger.success("API GET request successful")
                logger.performance_metric("API GET Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"API GET failed with status {response.status_code}")
    
    @task(2)
    def post_data(self):
        """POST request - medium frequency"""
        with logger.performance_context("API POST Request"):
            payload = {
                "name": f"Test User {random.randint(1, 1000)}",
                "email": f"user{random.randint(1, 1000)}@example.com",
                "message": "This is a test message"
            }
            
            response = self.client.post("/api/data", json=payload)
            
            if response.status_code in [200, 201]:
                logger.success("API POST request successful")
                logger.performance_metric("API POST Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"API POST failed with status {response.status_code}")
    
    @task(1)
    def update_data(self):
        """PUT request - low frequency"""
        with logger.performance_context("API PUT Request"):
            item_id = random.randint(1, 100)
            payload = {
                "name": f"Updated User {item_id}",
                "email": f"updated{item_id}@example.com"
            }
            
            response = self.client.put(f"/api/data/{item_id}", json=payload)
            
            if response.status_code in [200, 204]:
                logger.success(f"API PUT request for item {item_id} successful")
                logger.performance_metric("API PUT Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"API PUT failed with status {response.status_code}")


class EcommerceUser(HttpUser):
    """
    Simulates e-commerce user behavior
    Includes shopping cart and checkout flows
    """
    
    wait_time = between(2, 5)  # Slower, more realistic e-commerce behavior
    
    def on_start(self):
        """Called when a user starts"""
        logger.info(f"E-commerce User {self.client.base_url} started shopping")
    
    @task(5)
    def browse_catalog(self):
        """Browse product catalog"""
        with logger.performance_context("Catalog Browse"):
            response = self.client.get("/catalog")
            
            if response.status_code == 200:
                logger.success("Catalog browsed successfully")
                logger.performance_metric("Catalog Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Catalog browse failed with status {response.status_code}")
    
    @task(3)
    def add_to_cart(self):
        """Add item to shopping cart"""
        with logger.performance_context("Add to Cart"):
            product_id = random.randint(1, 50)
            quantity = random.randint(1, 3)
            
            payload = {
                "product_id": product_id,
                "quantity": quantity
            }
            
            response = self.client.post("/cart/add", json=payload)
            
            if response.status_code == 200:
                logger.success(f"Added product {product_id} to cart successfully")
                logger.performance_metric("Add to Cart Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Add to cart failed with status {response.status_code}")
    
    @task(2)
    def view_cart(self):
        """View shopping cart"""
        with logger.performance_context("View Cart"):
            response = self.client.get("/cart")
            
            if response.status_code == 200:
                logger.success("Cart viewed successfully")
                logger.performance_metric("View Cart Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"View cart failed with status {response.status_code}")
    
    @task(1)
    def checkout_process(self):
        """Complete checkout process"""
        with logger.performance_context("Checkout Process"):
            # Simulate multi-step checkout
            checkout_data = {
                "shipping_address": {
                    "name": f"Test User {random.randint(1, 1000)}",
                    "address": "123 Test Street",
                    "city": "Test City",
                    "zip": "12345"
                },
                "payment_method": "credit_card",
                "card_number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123"
            }
            
            # Step 1: Submit shipping info
            response1 = self.client.post("/checkout/shipping", json=checkout_data["shipping_address"])
            
            if response1.status_code == 200:
                logger.success("Shipping information submitted successfully")
                
                # Step 2: Submit payment info
                response2 = self.client.post("/checkout/payment", json=checkout_data)
                
                if response2.status_code == 200:
                    logger.success("Checkout completed successfully")
                    logger.performance_metric("Checkout Response Time", 
                                            response1.elapsed.total_seconds() + response2.elapsed.total_seconds(), "s")
                else:
                    logger.error(f"Payment submission failed with status {response2.status_code}")
            else:
                logger.error(f"Shipping submission failed with status {response1.status_code}")


# Event handlers for Locust
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when the test starts"""
    logger.start_test("Locust Load Test", "performance")
    logger.info(f"Load test started with {environment.runner.user_count} users")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when the test stops"""
    logger.end_test("Locust Load Test")
    logger.info("Load test completed")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, start_time, url, **kwargs):
    """Called for every request"""
    if exception:
        logger.error(f"Request failed: {name} - {exception}")
    else:
        logger.performance_metric(f"{request_type} {name}", response_time / 1000, "s")  # Convert to seconds


# Custom test scenarios
class StressTestUser(HttpUser):
    """
    Stress test user - generates high load
    Used for finding breaking points
    """
    
    wait_time = between(0.1, 0.5)  # Very fast requests for stress testing
    
    @task(10)
    def rapid_requests(self):
        """Make rapid requests to stress the system"""
        with logger.performance_context("Stress Request"):
            response = self.client.get("/")
            
            if response.status_code == 200:
                logger.performance_metric("Stress Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Stress request failed with status {response.status_code}")


class SpikeTestUser(HttpUser):
    """
    Spike test user - simulates sudden traffic spikes
    """
    
    wait_time = between(0.05, 0.2)  # Extremely fast for spike testing
    
    @task(20)
    def spike_requests(self):
        """Make spike requests"""
        with logger.performance_context("Spike Request"):
            response = self.client.get("/api/health")
            
            if response.status_code == 200:
                logger.performance_metric("Spike Response Time", response.elapsed.total_seconds(), "s")
            else:
                logger.error(f"Spike request failed with status {response.status_code}")


# Configuration for different test scenarios
def get_test_config(scenario: str) -> Dict[str, Any]:
    """Get configuration for different test scenarios"""
    
    configs = {
        "smoke": {
            "users": 5,
            "spawn_rate": 1,
            "run_time": "60s"
        },
        "load": {
            "users": 50,
            "spawn_rate": 5,
            "run_time": "300s"
        },
        "stress": {
            "users": 200,
            "spawn_rate": 10,
            "run_time": "600s"
        },
        "spike": {
            "users": 100,
            "spawn_rate": 50,
            "run_time": "120s"
        },
        "endurance": {
            "users": 100,
            "spawn_rate": 5,
            "run_time": "3600s"  # 1 hour
        }
    }
    
    return configs.get(scenario, configs["load"])


# Example usage:
# locust -f locustfile.py --host=https://example.com --users=50 --spawn-rate=5 --run-time=300s

