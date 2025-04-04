from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.services.contacts import ContactsService
from src.app.response.schemas import ContactBase

class ContactsController:
  def __init__(self, db: AsyncSession):
    self.db = ContactsService(db)

  async def create_contact(self, contact: ContactBase):
      created_contact = await self.db.create_contact(contact)
      return ContactBase.from_orm(created_contact)

  async def get_contacts(self, skip: int = 0, limit: int = 10):
      contacts = await self.db.get_contacts(skip, limit)
      return {"contacts": [ContactBase.from_orm(contact) for contact in contacts]}

  async def get_by_id(self, id: int):
      contact = await self.db.get_by_id(id)
      if contact is None:
          return None
      return ContactBase.from_orm(contact)

  async def update_contact(self, id: int, contact: ContactBase):
      updated_contact = await self.db.update_contact(id, contact)  
      return ContactBase.from_orm(updated_contact)

  async def delete_contact(self, id: int):
      deleted_contact = await self.db.delete_contact(id)
      return ContactBase.from_orm(deleted_contact)

  async def search_contact(self, name: str = None, surname: str = None, email: str = None):
    contacts = await self.db.search_contacts(name, surname, email)
    return {"contacts": [ContactBase.from_orm(contact) for contact in contacts]}
  
  async def get_upcoming_birthdays(self):
    contacts = await self.db.get_upcoming_birthdays()
    return {"contacts": [ContactBase.from_orm(contact) for contact in contacts]}