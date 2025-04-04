from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, and_
from datetime import datetime, timedelta, timezone

from src.app.database.models import Contact
from src.app.response.schemas import ContactBase


class ContactsService:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def create_contact(self, contact: ContactBase):
    if contact is None:
        raise ValueError("Contact cannot be None.")
    new_contact = Contact(name=contact.name, surname=contact.surname, email=contact.email, phone=contact.phone, birthdate=self.str_to_date(contact.birthdate), notes=contact.notes)
    try:
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
    except Exception as e:
        await self.session.rollback()
        raise RuntimeError(f"An error occurred while creating the contact: {e}")
    
    return new_contact

  async def get_contacts(self, skip: int = 0, limit: int = 10):
    stmt = select(Contact).offset(skip).limit(limit)
    result = await self.session.execute(stmt)
    if result is None:
        raise ValueError("No contacts found.")
    return result.scalars().all()
  
  async def get_by_id(self, id: int):
    stmt = select(Contact).where(Contact.id == id)
    result = await self.session.execute(stmt)
    contact = result.scalar_one_or_none()
    if result is None:
        raise ValueError(f"Contact with the given ID {id} does not exist.")
    return contact
  
  async def update_contact(self, id: int, contact: ContactBase):
    existing_contact = await self.get_by_id(id)
    if existing_contact is None:
        raise ValueError("Contact with the given ID does not exist.")
    
    if contact.name:
        existing_contact.name = contact.name
    if contact.email:
        existing_contact.email = contact.email
    if contact.phone:
        existing_contact.phone = contact.phone
    if contact.birthdate:
        existing_contact.birthdate = self.str_to_date(contact.birthdate)
    if contact.notes:
        existing_contact.notes = contact.notes
    try:
        self.session.add(existing_contact)
        await self.session.commit()
        await self.session.refresh(existing_contact)
    except Exception as e:
        await self.session.rollback()
        raise RuntimeError(f"Failed to update contact: {e}")
    
    return existing_contact
  
  async def delete_contact(self, id: int):
    try:
        contact = await self.get_by_id(id)
        print(contact, "Contact:", contact.name)
        if contact is None:
            raise ValueError(f"Contact with the given ID {id} does not exist.")
        await self.session.delete(contact)
        await self.session.commit()
        return contact
    except Exception as e:
        await self.session.rollback()
        raise RuntimeError(f"Failed to delete contact. {e}")
    
  async def search_contacts(self, name: str = None, surname: str = None, email: str = None):
    stmt = select(Contact)
    
    if name:
        stmt = stmt.filter(Contact.name.ilike(f"%{name}%"))
    if surname:
        stmt = stmt.filter(Contact.surname.ilike(f"%{surname}%"))
    if email:
        stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))

    result = await self.session.execute(stmt)
    return result.scalars().all()
  
  async def get_upcoming_birthdays(self):
    today = datetime.now(timezone.utc).date()
    next_week = today + timedelta(days=7)

    query = select(Contact).filter(
        and_(
            extract("month", Contact.birthdate) == today.month,
            extract("day", Contact.birthdate) >= today.day,
            extract("day", Contact.birthdate) < next_week.day
        ) | and_(
            extract("month", Contact.birthdate) == next_week.month,
            extract("day", Contact.birthdate) < next_week.day
        )
    )

    result = await self.session.execute(query)
    return result.scalars().all()
    
  @staticmethod
  def str_to_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None