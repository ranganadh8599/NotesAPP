from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid


class User(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    password: str
    created_on: Optional[datetime] = None
    last_update: Optional[datetime] = None


class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    password: str


class UserLogin(BaseModel):
    user_email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    created_on: datetime
    last_update: datetime


class Note(BaseModel):
    note_id: str
    note_title: str
    note_content: str
    user_id: str
    created_on: Optional[datetime] = None
    last_update: Optional[datetime] = None


class NoteCreate(BaseModel):
    note_title: str
    note_content: str


class NoteUpdate(BaseModel):
    note_title: Optional[str] = None
    note_content: Optional[str] = None


class NoteResponse(BaseModel):
    note_id: str
    note_title: str
    note_content: str
    user_id: str
    created_on: datetime
    last_update: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: Optional[str] = None


def generate_id():
    return str(uuid.uuid4())