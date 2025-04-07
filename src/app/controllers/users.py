from sqlalchemy.ext.asyncio import AsyncSession
from src.app.services.users import UserService
from src.app.response.schemas import UserCreate

class UserController:
  def __init__(self, db: AsyncSession):
    self.db = UserService(db)

  async def get_user_by_id(self, user_id: int):
    user = await self.db.get_user_by_id(user_id)
    return user
  
  async def get_user_by_username(self, name: str):
    user = await self.db.get_user_by_username(name)
    return user
  
  async def get_user_by_email(self, email: str):
    user = await self.db.get_user_by_email(email)
    return user
  
  async def create_user(self, body: UserCreate, avatar: str = None):
    user = await self.db.create_user(body, avatar)
    return user
  
  # async def update_user(self, user_id: int, body: UserUpdate):
  #   user = await self.db.update_user(user_id, body)
  #   return user
  
  async def delete_user(self, user_id: int):
    user = await self.db.delete_user(user_id)
    return user
  
  async def confirm_email(self, email: str):
    return await self.db.confirm_email(email)
  
  # async def reset_password(self, email: str):
  #   user = await self.db.reset_password(email)
  #   return user