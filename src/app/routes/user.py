from sqlalchemy.orm import Session
from fastapi import Depends, Request, File, UploadFile
from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.app.services.current_user import get_current_user
from src.app.response.schemas import User
from app.controllers.user import UserController
from src.app.database.db import get_db
from src.app.services.upload_file import UploadFileService
from src.app.config.config import settings

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/me", response_model=User, status_code=200)
@limiter.limit("10/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user

@router.patch("/avatar", response_model=User, status_code=200)
@limiter.limit("10/minute")
async def update_user(request: Request, file: UploadFile = File(), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    avatar_url = UploadFileService(
        settings.CLD_NAME, settings.CLD_API_KEY, settings.CLD_API_SECRET
    ).upload_file(file, user.name)

    user.avatar = avatar_url
    user_controller = UserController(db)
    
    return await user_controller.update_user(user.id, user)
