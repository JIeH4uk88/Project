from tkinter import Listbox
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributs=True)
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    phone_path: Optional[str] = None
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ValidationErrorDetail(BaseModel):
    loc: List
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    details: Optional[List[ValidationErrorDetail]] = None

class CommentResponse(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime

class NewsResponse(BaseModel):
    id: int
    title: str
    subtitle: Optional[str] = None
    text: str
    image_path: Optional[str] = None
    author: object
    image_url: Optional[str] = None
    tags: List
    created_at: datetime
    comments_count: int

class NewsListResponse(BaseModel):
    items: List[NewsResponse]
    total: int
    page: int
    per_page: int


