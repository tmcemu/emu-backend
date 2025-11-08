import io
from abc import abstractmethod
from typing import Protocol

from fastapi import Request

from internal import model
from internal.controller.http.handler.account.model import (
    ChangePasswordBody,
    DeleteTwoFaBody,
    LoginBody,
    RecoveryPasswordBody,
    RegisterBody,
    SetTwoFaBody,
    VerifyTwoFaBody,
)


class IAccountController(Protocol):
    @abstractmethod
    async def register(self, body: RegisterBody):
        pass

    @abstractmethod
    async def login(self, body: LoginBody):
        pass

    @abstractmethod
    async def change_password(self, request: Request, body: ChangePasswordBody):
        pass


class IAccountService(Protocol):
    @abstractmethod
    async def register(self, login: str, password: str, account_type: str) -> model.AuthorizationDataDTO:
        pass

    @abstractmethod
    async def login(
        self,
        login: str,
        password: str,
    ) -> model.AuthorizationDataDTO | None:
        pass


    @abstractmethod
    async def change_password(self, account_id: int, new_password: str, old_password: str) -> None:
        pass


class IAccountRepo(Protocol):
    @abstractmethod
    async def create_account(self, login: str, password: str, account_type: str) -> int:
        pass

    @abstractmethod
    async def account_by_id(self, account_id: int) -> list[model.Account]:
        pass

    @abstractmethod
    async def account_by_login(self, login: str) -> list[model.Account]:
        pass

    @abstractmethod
    async def update_password(self, account_id: int, new_password: str) -> None:
        pass
