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

    class Config:
        allow_population_by_alias = True
        fields = {
            'full_name': 'fullName',
            'is_active': 'isActive',
            'is_superuser': 'isSuperuser',
        }


class UserInDb(UserBaseInDb):
    hashed_password: str
