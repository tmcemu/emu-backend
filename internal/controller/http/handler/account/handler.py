from fastapi import Request
from fastapi.responses import JSONResponse

from internal import interface
from internal.common.error import ErrForbidden
from internal.controller.http.handler.account.model import (
    ChangePasswordBody,
    LoginBody,
    RegisterBody,
)
from pkg.log_wrapper import auto_log
from pkg.trace_wrapper import traced_method


class AccountController(interface.IAccountController):
    def __init__(
        self,
        tel: interface.ITelemetry,
        account_service: interface.IAccountService,
        interserver_secret_key: str,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.account_service = account_service
        self.interserver_secret_key = interserver_secret_key

    @auto_log()
    @traced_method()
    async def register(self, body: RegisterBody) -> JSONResponse:
        # Validate interserver secret key
        if body.interserver_secret_key != self.interserver_secret_key:
            raise ErrForbidden()

        authorization_data = await self.account_service.register(
            login=body.login,
            password=body.password,
            account_type=body.account_type
        )

        response = JSONResponse(status_code=201, content={"account_id": authorization_data.account_id})

        response.set_cookie(
            key="Access-Token", value=authorization_data.access_token, httponly=True, secure=True, samesite="lax"
        )
        response.set_cookie(
            key="Refresh-Token",
            value=authorization_data.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        return response

    @auto_log()
    @traced_method()
    async def login(self, body: LoginBody) -> JSONResponse:
        authorization_data = await self.account_service.login(login=body.login, password=body.password)

        response = JSONResponse(status_code=200, content={
            "account_id": authorization_data.account_id,
            "account_type": authorization_data.account_type
        })

        response.set_cookie(
            key="Access-Token", value=authorization_data.access_token, httponly=True, secure=True, samesite="lax"
        )
        response.set_cookie(
            key="Refresh-Token", value=authorization_data.refresh_token, httponly=True, secure=True, samesite="lax"
        )

        return response

    @auto_log()
    @traced_method()
    async def change_password(self, request: Request, body: ChangePasswordBody) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id

        if account_id == 0:
            return JSONResponse(status_code=403, content={})

        await self.account_service.change_password(
            account_id=account_id, new_password=body.new_password, old_password=body.old_password
        )

        return JSONResponse(status_code=200, content={})
