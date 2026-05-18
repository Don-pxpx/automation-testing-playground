"""
JSONPlaceholder API Endpoint Tests
Comprehensive test suite for JSONPlaceholder API endpoints with verification
"""

import pytest
from faker import Faker
from automation_testing_playground.pages.api.jsonplaceholder_client import JSONPlaceholderClient
from automation_testing_playground.config.api_config import JSONPlaceholderEndpoints
from automation_testing_playground.helpers.log_helpers import InlineLogger

fake = Faker()


class TestJSONPlaceholderEndpoints:
    """Test class for JSONPlaceholder API endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.client = JSONPlaceholderClient()
        self.logger = InlineLogger()
    
    def test_get_all_posts(self):
        """Test GET /posts endpoint - retrieve all posts"""
        self.logger.test_start("Get All Posts Test")
        
        # Get all posts
        posts = self.client.get_all_posts()
        
        # Verify response structure
        self.logger.step("Verify posts response structure")
        assert isinstance(posts, list), "Posts should be a list"
        assert len(posts) > 0, "Should return at least one post"
        
        # Verify first post schema
        if posts:
            first_post = posts[0]
            assert self.client.verify_post_schema(first_post), "First post should match expected schema"
        
        # Verify response time
        response = self.client.get(JSONPlaceholderEndpoints.POSTS)
        assert self.client.verify_response_time(response, max_time=3.0), "Response time should be acceptable"
        
        self.logger.success(f"Successfully retrieved {len(posts)} posts")
        self.logger.test_end("Get All Posts Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_get_post_by_id(self):
        """Test GET /posts/{id} endpoint - retrieve specific post"""
        self.logger.test_start("Get Post By ID Test")
        
        # Test with a known post ID
        post_id = 1
        post = self.client.get_post_by_id(post_id)
        
        # Verify post data
        self.logger.step("Verify post data")
        assert post['id'] == post_id, f"Post ID should be {post_id}"
        assert 'title' in post, "Post should have title"
        assert 'body' in post, "Post should have body"
        assert 'userId' in post, "Post should have userId"
        
        # Verify schema
        assert self.client.verify_post_schema(post), "Post should match expected schema"
        
        # Test with non-existent post ID
        self.logger.step("Test with non-existent post ID")
        response = self.client.get(JSONPlaceholderEndpoints.POST_BY_ID.format(id=99999))
        assert self.client.verify_status_code(response, 404), "Should return 404 for non-existent post"
        
        self.logger.success(f"Successfully retrieved post with ID: {post_id}")
        self.logger.test_end("Get Post By ID Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_create_post(self):
        """Test POST /posts endpoint - create new post"""
        self.logger.test_start("Create Post Test")
        
        # Generate test data
        title = fake.sentence()
        body = fake.text()
        user_id = 1
        
        self.logger.step(f"Create post with title: {title}")
        
        # Create new post
        new_post = self.client.create_post(title, body, user_id)
        
        # Verify response
        assert new_post['title'] == title, "Post title should match"
        assert new_post['body'] == body, "Post body should match"
        assert new_post['userId'] == user_id, "User ID should match"
        assert 'id' in new_post, "Response should include post ID"
        
        # Verify schema
        assert self.client.verify_post_schema(new_post), "Created post should match expected schema"
        
        self.logger.success(f"Successfully created post with ID: {new_post.get('id', 'N/A')}")
        self.logger.test_end("Create Post Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_update_post(self):
        """Test PUT /posts/{id} endpoint - update existing post"""
        self.logger.test_start("Update Post Test")
        
        # Generate test data
        post_id = 1
        new_title = fake.sentence()
        new_body = fake.text()
        user_id = 1
        
        self.logger.step(f"Update post with ID: {post_id}")
        
        # Update post
        updated_post = self.client.update_post(post_id, new_title, new_body, user_id)
        
        # Verify response
        assert updated_post['id'] == post_id, "Post ID should remain the same"
        assert updated_post['title'] == new_title, "Post title should be updated"
        assert updated_post['body'] == new_body, "Post body should be updated"
        assert updated_post['userId'] == user_id, "User ID should match"
        
        # Verify schema
        assert self.client.verify_post_schema(updated_post), "Updated post should match expected schema"
        
        self.logger.success(f"Successfully updated post with ID: {post_id}")
        self.logger.test_end("Update Post Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_patch_post(self):
        """Test PATCH /posts/{id} endpoint - partially update post"""
        self.logger.test_start("Patch Post Test")
        
        # Generate test data
        post_id = 1
        new_title = fake.sentence()
        
        self.logger.step(f"Patch post with ID: {post_id}")
        
        # Partially update post
        patched_post = self.client.patch_post(post_id, title=new_title)
        
        # Verify response
        assert patched_post['id'] == post_id, "Post ID should remain the same"
        assert patched_post['title'] == new_title, "Post title should be updated"
        assert 'body' in patched_post, "Post body should still exist"
        assert 'userId' in patched_post, "User ID should still exist"
        
        # Verify schema
        assert self.client.verify_post_schema(patched_post), "Patched post should match expected schema"
        
        self.logger.success(f"Successfully patched post with ID: {post_id}")
        self.logger.test_end("Patch Post Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_delete_post(self):
        """Test DELETE /posts/{id} endpoint - delete post"""
        self.logger.test_start("Delete Post Test")
        
        post_id = 1
        
        self.logger.step(f"Delete post with ID: {post_id}")
        
        # Delete post
        result = self.client.delete_post(post_id)
        
        # Verify response
        assert result is True, "Delete operation should return True"
        
        self.logger.success(f"Successfully deleted post with ID: {post_id}")
        self.logger.test_end("Delete Post Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_get_all_users(self):
        """Test GET /users endpoint - retrieve all users"""
        self.logger.test_start("Get All Users Test")
        
        # Get all users
        users = self.client.get_all_users()
        
        # Verify response structure
        self.logger.step("Verify users response structure")
        assert isinstance(users, list), "Users should be a list"
        assert len(users) > 0, "Should return at least one user"
        
        # Verify first user schema
        if users:
            first_user = users[0]
            assert self.client.verify_user_schema(first_user), "First user should match expected schema"
        
        self.logger.success(f"Successfully retrieved {len(users)} users")
        self.logger.test_end("Get All Users Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_get_user_by_id(self):
        """Test GET /users/{id} endpoint - retrieve specific user"""
        self.logger.test_start("Get User By ID Test")
        
        # Test with a known user ID
        user_id = 1
        user = self.client.get_user_by_id(user_id)
        
        # Verify user data
        self.logger.step("Verify user data")
        assert user['id'] == user_id, f"User ID should be {user_id}"
        assert 'name' in user, "User should have name"
        assert 'username' in user, "User should have username"
        assert 'email' in user, "User should have email"
        
        # Verify schema
        assert self.client.verify_user_schema(user), "User should match expected schema"
        
        self.logger.success(f"Successfully retrieved user with ID: {user_id}")
        self.logger.test_end("Get User By ID Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_get_comments_by_post(self):
        """Test GET /posts/{post_id}/comments endpoint - retrieve comments for post"""
        self.logger.test_start("Get Comments By Post Test")
        
        # Test with a known post ID
        post_id = 1
        comments = self.client.get_comments_by_post(post_id)
        
        # Verify response structure
        self.logger.step("Verify comments response structure")
        assert isinstance(comments, list), "Comments should be a list"
        
        # Verify comment structure if comments exist
        if comments:
            first_comment = comments[0]
            assert 'id' in first_comment, "Comment should have ID"
            assert 'postId' in first_comment, "Comment should have postId"
            assert 'name' in first_comment, "Comment should have name"
            assert 'email' in first_comment, "Comment should have email"
            assert 'body' in first_comment, "Comment should have body"
        
        self.logger.success(f"Successfully retrieved {len(comments)} comments for post {post_id}")
        self.logger.test_end("Get Comments By Post Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_jsonpath_extraction(self):
        """Test JSONPath extraction from API responses"""
        self.logger.test_start("JSONPath Extraction Test")
        
        # Get all posts
        response = self.client.get(JSONPlaceholderEndpoints.POSTS)
        
        # Extract values using JSONPath
        self.logger.step("Extract values using JSONPath")
        
        # Extract all post titles
        titles = self.client.extract_value_by_jsonpath(response, "$[*].title")
        assert isinstance(titles, list), "Should extract list of titles"
        assert len(titles) > 0, "Should extract at least one title"
        
        # Extract first post ID
        first_id = self.client.extract_value_by_jsonpath(response, "$[0].id")
        assert isinstance(first_id, int), "Should extract integer ID"
        assert first_id == 1, "First post ID should be 1"
        
        # Extract user IDs
        user_ids = self.client.extract_value_by_jsonpath(response, "$[*].userId")
        assert isinstance(user_ids, list), "Should extract list of user IDs"
        
        self.logger.success("Successfully extracted values using JSONPath")
        self.logger.test_end("JSONPath Extraction Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
    
    def test_response_validation(self):
        """Test comprehensive response validation"""
        self.logger.test_start("Response Validation Test")
        
        # Test status code validation
        self.logger.step("Test status code validation")
        response = self.client.get(JSONPlaceholderEndpoints.POSTS)
        assert self.client.verify_status_code(response, 200), "Should return 200 status"
        
        # Test response time validation
        self.logger.step("Test response time validation")
        assert self.client.verify_response_time(response, max_time=5.0), "Response time should be acceptable"
        
        # Test response content validation
        self.logger.step("Test response content validation")
        expected_content = {"id": 1, "userId": 1}
        response = self.client.get(JSONPlaceholderEndpoints.POST_BY_ID.format(id=1))
        assert self.client.verify_response_contains(response, expected_content), "Response should contain expected content"
        
        # Test error handling
        self.logger.step("Test error handling")
        response = self.client.get(JSONPlaceholderEndpoints.POST_BY_ID.format(id=99999))
        assert self.client.verify_status_code(response, 404), "Should return 404 for non-existent resource"
        
        self.logger.success("All response validation tests passed")
        self.logger.test_end("Response Validation Test", "passed")
        self.logger.summary(passed=1, failed=0, skipped=0)
