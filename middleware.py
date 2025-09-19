from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
from typing import Dict
import asyncio

# Simple in-memory rate limiter (use Redis in production)
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def is_allowed(self, client_ip: str) -> bool:
        """Check if client is within rate limit"""
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if req_time > minute_ago
        ]
        
        # Check current count
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[client_ip].append(current_time)
        return True

rate_limiter = RateLimiter(requests_per_minute=60)

async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    client_ip = request.client.host if request.client else "unknown"
    
    # Skip rate limiting for health endpoints
    if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    if not await rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": f"Maximum {rate_limiter.requests_per_minute} requests per minute allowed",
                "retry_after": 60
            },
            headers={"Retry-After": "60"}
        )
    
    return await call_next(request)

async def error_handler_middleware(request: Request, call_next):
    """Global error handling middleware"""
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions to let FastAPI handle them
        raise
    except Exception as e:
        # Handle unexpected errors
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "detail": str(e) if request.app.debug else None
            }
        )

# Input validation helpers
def validate_temperature(temperature: float) -> float:
    """Validate temperature parameter"""
    if not 0.0 <= temperature <= 2.0:
        raise HTTPException(
            status_code=400, 
            detail="Temperature must be between 0.0 and 2.0"
        )
    return temperature

def validate_max_tokens(max_tokens: int) -> int:
    """Validate max_tokens parameter"""
    if not 1 <= max_tokens <= 4000:
        raise HTTPException(
            status_code=400, 
            detail="max_tokens must be between 1 and 4000"
        )
    return max_tokens

def validate_model(model: str) -> str:
    """Validate model parameter"""
    allowed_models = [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-instruct",
        "gpt-4",
        "gpt-4-1106-preview"
    ]
    
    if model not in allowed_models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model}' not supported. Allowed models: {', '.join(allowed_models)}"
        )
    return model