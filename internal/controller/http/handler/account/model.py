from pydantic import BaseModel


class RegisterBody(BaseModel):
    login: str
    password: str
    account_type: str
    interserver_secret_key: str


class LoginBody(BaseModel):
    login: str
    password: str


class ChangePasswordBody(BaseModel):
    old_password: str
    new_password: str
