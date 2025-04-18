from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database.models import User
from src.app.response.schemas import UserCreate
from sqlalchemy import select


class UserService:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).filter_by(name=username)
        user = await self.db.execute(stmt)
        return user.scalar()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        user = User(**body.model_dump(exclude_unset=True), avatar=avatar)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        await self.db.delete(User, user_id)
        await self.db.commit()
        return

    async def confirm_email(self, email: str):
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_user(self, user_id: int, body: User):
        user = await self.get_user_by_id(user_id)
        if body.name:
            user.name = body.name
        if body.email:
            user.email = body.email 
        if body.password:
            user.password = body.password
        if body.avatar:
            user.avatar = body.avatar
        await self.db.commit()
        await self.db.refresh(user)
        return user