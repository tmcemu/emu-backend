from pydantic import BaseModel

class AuthorizationBody(BaseModel):
    account_id: int
    account_type: str

class AuthorizationResponse(BaseModel):
    access_token: str
    refresh_token: str

class CheckAuthorizationResponse(BaseModel):
    account_id: int
    account_type: str
    message: str
    status_code: int