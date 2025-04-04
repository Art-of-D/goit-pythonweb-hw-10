from typing import Optional, List
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: str = Field(max_length=150)
    phone: str = Field(max_length=20)
    birthdate: str
    notes: Optional[str] = None

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            surname=obj.surname,
            email=obj.email,
            phone=obj.phone,
            birthdate=obj.birthdate.strftime("%Y-%m-%d"),
            notes=obj.notes,
        )
    
class ContactListResponse(BaseModel):
    contacts: List[ContactBase]