from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.services.contacts import ContactsService
from src.app.response.schemas import ContactBase, ContactCreate

class ContactsController:
  def __init__(self, db: AsyncSession):
    self.db = ContactsService(db)

  async def create_contact(self, contact: ContactCreate):
      created_contact = await self.db.create_contact(contact)
      return ContactCreate.from_orm(created_contact)

  async def get_contacts(self, user_id: int, skip: int = 0, limit: int = 10):
      contacts = await self.db.get_contacts(user_id, skip, limit)
      return {"contacts": [ContactBase.from_orm(contact) for contact in contacts]}

  async def get_by_id(self, user_id: int, id: int):
      contact = await self.db.get_by_id(user_id, id)
      if contact is None:
          return None
      return ContactBase.from_orm(contact)

  async def update_contact(self, user_id: int, id: int, contact: ContactBase):
      updated_contact = await self.db.update_contact(user_id, id, contact)  
      return ContactBase.from_orm(updated_contact)

  async def delete_contact(self, user_id: int, id: int):
      deleted_contact = await self.db.delete_contact(user_id, id)
      return ContactBase.from_orm(deleted_contact)

  async def search_contact(self, user_id: int, name: str = None, surname: str = None, email: str = None):
    contacts = await self.db.search_contacts(user_id, name, surname, email)
    return {"contacts": [ContactBase.from_orm(contact) for contact in contacts]}
  
  async def get_upcoming_birthdays(self, user_id: int):
    contacts = await self.db.get_upcoming_birthdays(user_id)
    return {"contacts": [ContactBase.from_orm(contact) for contact in contacts]}