from pydantic import BaseModel


class SystemUser(BaseModel):
    ...


class TokenPayload(BaseModel):
    from datetime import datetime
    sub: str
    exp: datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
