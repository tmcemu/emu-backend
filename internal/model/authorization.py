from dataclasses import dataclass


@dataclass
class JWTToken:
    access_token: str
    refresh_token: str


@dataclass
class TokenPayload:
    account_id: int
    account_type: str
    exp: int