"""
JSONPlaceholder API Client for Automation Testing Playground
Provides specific methods for testing JSONPlaceholder API endpoints
"""

from typing import Dict, Any, Optional, List
from pages.api.base_api_client import BaseAPIClient
from config.api_config import APIConfig, JSONPlaceholderEndpoints


class JSONPlaceholderClient(BaseAPIClient):
    """API client for JSONPlaceholder endpoints"""
    
    def __init__(self):
        """Initialize JSONPlaceholder client"""
        super().__init__(APIConfig.JSONPLACEHOLDER_BASE_URL)
    
    # Posts endpoints
    def get_all_posts(self) -> Dict[str, Any]:
        """Get all posts"""
        self.logger.step("Get all posts from JSONPlaceholder")
        response = self.get(JSONPlaceholderEndpoints.POSTS)
        self.verify_status_code(response, 200)
        return response.json()
    
    def get_post_by_id(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post by ID"""
        self.logger.step(f"Get post with ID: {post_id}")
        endpoint = JSONPlaceholderEndpoints.POST_BY_ID.format(id=post_id)
        response = self.get(endpoint)
        self.verify_status_code(response, 200)
        return response.json()
    
    def create_post(self, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """Create a new post"""
        self.logger.step(f"Create new post with title: {title}")
        post_data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = self.post(JSONPlaceholderEndpoints.POSTS, post_data)
        self.verify_status_code(response, 201)
        return response.json()
    
    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """Update an existing post"""
        self.logger.step(f"Update post with ID: {post_id}")
        endpoint = JSONPlaceholderEndpoints.POST_BY_ID.format(id=post_id)
        post_data = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = self.put(endpoint, post_data)
        self.verify_status_code(response, 200)
        return response.json()
    
    def patch_post(self, post_id: int, **fields) -> Dict[str, Any]:
        """Partially update a post"""
        self.logger.step(f"Patch post with ID: {post_id}")
        endpoint = JSONPlaceholderEndpoints.POST_BY_ID.format(id=post_id)
        response = self.patch(endpoint, fields)
        self.verify_status_code(response, 200)
        return response.json()
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        self.logger.step(f"Delete post with ID: {post_id}")
        endpoint = JSONPlaceholderEndpoints.POST_BY_ID.format(id=post_id)
        response = self.delete(endpoint)
        self.verify_status_code(response, 200)
        return True
    
    # Users endpoints
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        self.logger.step("Get all users from JSONPlaceholder")
        response = self.get(JSONPlaceholderEndpoints.USERS)
        self.verify_status_code(response, 200)
        return response.json()
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID"""
        self.logger.step(f"Get user with ID: {user_id}")
        endpoint = JSONPlaceholderEndpoints.USER_BY_ID.format(id=user_id)
        response = self.get(endpoint)
        self.verify_status_code(response, 200)
        return response.json()
    
    # Comments endpoints
    def get_all_comments(self) -> List[Dict[str, Any]]:
        """Get all comments"""
        self.logger.step("Get all comments from JSONPlaceholder")
        response = self.get(JSONPlaceholderEndpoints.COMMENTS)
        self.verify_status_code(response, 200)
        return response.json()
    
    def get_comments_by_post(self, post_id: int) -> List[Dict[str, Any]]:
        """Get comments for a specific post"""
        self.logger.step(f"Get comments for post ID: {post_id}")
        endpoint = JSONPlaceholderEndpoints.COMMENTS_BY_POST.format(post_id=post_id)
        response = self.get(endpoint)
        self.verify_status_code(response, 200)
        return response.json()
    
    # Albums endpoints
    def get_all_albums(self) -> List[Dict[str, Any]]:
        """Get all albums"""
        self.logger.step("Get all albums from JSONPlaceholder")
        response = self.get(JSONPlaceholderEndpoints.ALBUMS)
        self.verify_status_code(response, 200)
        return response.json()
    
    def get_albums_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get albums for a specific user"""
        self.logger.step(f"Get albums for user ID: {user_id}")
        endpoint = JSONPlaceholderEndpoints.ALBUMS_BY_USER.format(user_id=user_id)
        response = self.get(endpoint)
        self.verify_status_code(response, 200)
        return response.json()
    
    # Photos endpoints
    def get_all_photos(self) -> List[Dict[str, Any]]:
        """Get all photos"""
        self.logger.step("Get all photos from JSONPlaceholder")
        response = self.get(JSONPlaceholderEndpoints.PHOTOS)
        self.verify_status_code(response, 200)
        return response.json()
    
    def get_photos_by_album(self, album_id: int) -> List[Dict[str, Any]]:
        """Get photos for a specific album"""
        self.logger.step(f"Get photos for album ID: {album_id}")
        endpoint = JSONPlaceholderEndpoints.PHOTOS_BY_ALBUM.format(album_id=album_id)
        response = self.get(endpoint)
        self.verify_status_code(response, 200)
        return response.json()
    
    # Todos endpoints
    def get_all_todos(self) -> List[Dict[str, Any]]:
        """Get all todos"""
        self.logger.step("Get all todos from JSONPlaceholder")
        response = self.get(JSONPlaceholderEndpoints.TODOS)
        self.verify_status_code(response, 200)
        return response.json()
    
    def get_todos_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get todos for a specific user"""
        self.logger.step(f"Get todos for user ID: {user_id}")
        endpoint = JSONPlaceholderEndpoints.TODOS_BY_USER.format(user_id=user_id)
        response = self.get(endpoint)
        self.verify_status_code(response, 200)
        return response.json()
    
    # Validation methods
    def verify_post_schema(self, post: Dict[str, Any]) -> bool:
        """Verify that a post has the correct schema"""
        post_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "body": {"type": "string"},
                "userId": {"type": "integer"}
            },
            "required": ["id", "title", "body", "userId"]
        }
        
        # Create a mock response object with proper json method
        class MockResponse:
            def __init__(self, data):
                self._data = data
            def json(self):
                return self._data
        
        response = MockResponse(post)
        return self.verify_json_schema(response, post_schema)
    
    def verify_user_schema(self, user: Dict[str, Any]) -> bool:
        """Verify that a user has the correct schema"""
        user_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "username": {"type": "string"},
                "email": {"type": "string"},
                "address": {"type": "object"},
                "phone": {"type": "string"},
                "website": {"type": "string"},
                "company": {"type": "object"}
            },
            "required": ["id", "name", "username", "email"]
        }
        
        # Create a mock response object with proper json method
        class MockResponse:
            def __init__(self, data):
                self._data = data
            def json(self):
                return self._data
        
        response = MockResponse(user)
        return self.verify_json_schema(response, user_schema)
