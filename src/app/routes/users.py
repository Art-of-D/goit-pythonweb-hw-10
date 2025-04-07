from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.app.response.schemas import User
from src.app.controllers.users import UserController
from src.app.database.db import get_db

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/me", response_model=User, status_code=200)
@limiter.limit("10/minute")
async def me():
  return "It`s me you looking for"