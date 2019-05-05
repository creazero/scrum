from pydantic import BaseModel


class Token(BaseModel):
    token: str = None


class TokenPayload(BaseModel):
    user_id: int = None
