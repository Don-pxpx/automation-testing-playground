"""
API Configuration for Automation Testing Playground
Contains base URLs, endpoints, and common settings for API testing
"""

class APIConfig:
    """Base API configuration class"""
    
    # JSONPlaceholder API (public test API)
    JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"
    
    # ReqRes API (another public test API)
    REQRES_BASE_URL = "https://reqres.in/api"
    
    # HTTPBin API (for testing HTTP methods)
    HTTPBIN_BASE_URL = "https://httpbin.org"
    
    # Common headers
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Automation-Testing-Playground/1.0"
    }
    
    # Timeout settings
    REQUEST_TIMEOUT = 30
    RESPONSE_TIMEOUT = 10
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1

class JSONPlaceholderEndpoints:
    """JSONPlaceholder API endpoints"""
    
    # Posts
    POSTS = "/posts"
    POST_BY_ID = "/posts/{id}"
    
    # Comments
    COMMENTS = "/comments"
    COMMENTS_BY_POST = "/posts/{post_id}/comments"
    
    # Users
    USERS = "/users"
    USER_BY_ID = "/users/{id}"
    
    # Albums
    ALBUMS = "/albums"
    ALBUMS_BY_USER = "/users/{user_id}/albums"
    
    # Photos
    PHOTOS = "/photos"
    PHOTOS_BY_ALBUM = "/albums/{album_id}/photos"
    
    # Todos
    TODOS = "/todos"
    TODOS_BY_USER = "/users/{user_id}/todos"

class ReqResEndpoints:
    """ReqRes API endpoints"""
    
    # Users
    USERS = "/users"
    USER_BY_ID = "/users/{id}"
    CREATE_USER = "/users"
    UPDATE_USER = "/users/{id}"
    DELETE_USER = "/users/{id}"
    
    # Authentication
    LOGIN = "/login"
    REGISTER = "/register"

class HTTPBinEndpoints:
    """HTTPBin API endpoints"""
    
    # HTTP Methods
    GET = "/get"
    POST = "/post"
    PUT = "/put"
    DELETE = "/delete"
    PATCH = "/patch"
    
    # Status Codes
    STATUS = "/status/{code}"
    
    # Headers
    HEADERS = "/headers"
    
    # Response
    JSON = "/json"
    XML = "/xml"
    
    # Authentication
    BASIC_AUTH = "/basic-auth/{user}/{passwd}"
    BEARER_AUTH = "/bearer"
    
    # Delays
    DELAY = "/delay/{seconds}"
    
    # Stream
    STREAM = "/stream/{n}"
