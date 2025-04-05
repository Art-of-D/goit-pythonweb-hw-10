from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database.db import get_db
from src.app.response.schemas import ContactBase, ContactListResponse
from src.app.controllers.contacts import ContactsController
from src.app.services.auth import get_current_user
from src.app.response.schemas import User


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=ContactListResponse)
async def read_contacts(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    contacts = ContactsController(db)
    return await contacts.get_contacts(skip, limit)


@router.get("/{contact_id}", response_model=ContactBase)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_controller = ContactsController(db)
    contact = await contact_controller.get_by_id(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.post("/", response_model=ContactBase, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    conctact_controller = ContactsController(db)
    try: 
        body.user_id = current_user.id
        contact = await conctact_controller.create_contact(body)
        return contact
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.put("/{contact_id}", response_model=ContactBase)
async def update_note(
    body: ContactBase, contact_id: int, db: AsyncSession = Depends(get_db)
):
    contact_controller = ContactsController(db)
    contact = await contact_controller.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactBase)
async def remove_conctact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_controller = ContactsController(db)
    contact = await contact_controller.delete_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact

@router.get("/contacts/search")
async def search_contacts(
    name: str = None, surname: str = None, email: str = None, db: AsyncSession = Depends(get_db)
):
    contact_controller = ContactsController(db)
    contact = await contact_controller.search_contact(name, surname, email)
    return contact

@router.get("/contacts/upcoming-birthdays")
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contact_controller = ContactsController(db)
    birthdays = await contact_controller.get_upcoming_birthdays()
    return birthdays