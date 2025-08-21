from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import List, Dict, Optional, Annotated
from enum import Enum


class RegisterRequest(BaseModel):
    firstname: Annotated[str, constr(strip_whitespace=True, min_length=2, max_length=50)]
    lastname: Annotated[str, constr(strip_whitespace=True, min_length=2, max_length=50)]
    email: EmailStr
    mobile: Annotated[str, constr(strip_whitespace=True, min_length=10, max_length=15)]
    password: Annotated[str, constr(min_length=6, max_length=50)]

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    mobile: str

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SlotsResponse(BaseModel):
    date: date
    slots: Dict

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class BookAppointmentRequest(BaseModel):
    date: date
    slot_time: str  # must be one of DEFAULT_SLOTS
    issue: str
    age: int
    gender: GenderEnum
    issue_duration: str

class AppointmentResponse(BaseModel):
    id: int
    date: date
    slot_time: str
    issue: str
    age: int
    gender: str
    issue_duration: str
    user_id: int

    class Config:
        orm_mode = True

