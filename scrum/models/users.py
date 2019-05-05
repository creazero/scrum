from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str = None


class UserAuth(UserBase):
    password: str


class UserBaseInDb(UserBase):
    id: int = None
    full_name: str = None
    is_active: bool = True
    is_superuser: bool = False


# update
class UserUpdate(UserBaseInDb):
    password: Optional[str] = None


# retrieve
class User(UserBaseInDb):
    pass


class UserInDb(UserBaseInDb):
    hashed_password: str
