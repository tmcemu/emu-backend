from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class AuthorizationDataDTO:
    account_id: int
    access_token: str
    refresh_token: str


class AuthorizationData(BaseModel):
    account_id: int
    account_type: str
    message: str
    status_code: int


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str
