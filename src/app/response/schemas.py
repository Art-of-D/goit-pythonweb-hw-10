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


class ContactCreate(ContactBase):
    user_id: int

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
            user_id=obj.user_id,
        )


class ContactListResponse(BaseModel):
    contacts: List[ContactBase]


class User(BaseModel):
    id: int
    name: str
    email: str
    avatar: Optional[str]


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class ConfirmResponse(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str
