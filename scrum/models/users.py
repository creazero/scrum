from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str = None
    full_name: str = None
    is_active: bool = True
    is_superuser: bool = False


class UserBaseInDb(UserBase):
    id: int = None


# create
class UserCreate(UserBase):
    password: str


# update
class UserUpdate(UserBaseInDb):
    password: Optional[str] = None


# retrieve
class User(UserBaseInDb):
    pass


class UserInDb(UserBaseInDb):
    hashed_password: str
