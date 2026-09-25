# Authentication and Authorization for Apex Intelligence

from fastapi import Depends, HTTPException, status, Header
from typing import Optional
import os
import hmac
import hashlib
from datetime import datetime, timedelta
import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

class APIKeyAuth:
    """Simple API Key authentication for private server"""
    
    def __init__(self):
        self.api_key = os.getenv("APEX_API_KEY", "apex-secret-key-change-me")
    
    async def __call__(self, x_api_key: str = Header(None)) -> str:
        if not x_api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key missing"
            )
        
        if x_api_key != self.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        return x_api_key

api_key_auth = APIKeyAuth()

class JWTAuth:
    """JWT token authentication for API access"""
    
    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

jwt_auth = JWTAuth()
