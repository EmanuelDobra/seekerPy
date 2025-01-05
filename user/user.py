from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum

## Testing
class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    clerk = "clerk"
    user = "user"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
    nickname: Optional[str] = ""
    gender: Gender
    roles: List[Role]

class UserUpdateRequest(BaseModel):
    name: Optional[str]
    nickname: Optional[str]
    gender: Optional[Gender]
    roles: Optional[List[Role]]

## Actual
