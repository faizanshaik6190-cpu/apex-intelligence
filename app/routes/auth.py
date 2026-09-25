from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import api_key_auth, jwt_auth
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

class TokenRequest(BaseModel):
    username: str = "owner"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/token", response_model=TokenResponse)
async def login(request: TokenRequest, api_key: str = Depends(api_key_auth)):
    """
    Get JWT token for API access.
    
    This is a simplified auth. Production should use proper user management.
    """
    token_data = {
        "sub": request.username,
        "type": "access"
    }
    
    access_token = jwt_auth.create_token(
        data=token_data,
        expires_delta=timedelta(days=7)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 604800  # 7 days in seconds
    }

@router.get("/verify")
async def verify_token(api_key: str = Depends(api_key_auth)):
    """
    Verify API key is valid.
    """
    return {"status": "valid", "message": "API key is valid"}
