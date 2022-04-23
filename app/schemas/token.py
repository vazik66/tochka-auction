from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

    def __str__(self):
        return f"{self.token_type} {self.access_token}"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    is_superuser: Optional[bool] = None
