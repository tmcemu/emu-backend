import jwt
import time

from internal import interface, common, model
from pkg.trace_wrapper import traced_method


class AuthorizationService(interface.IAuthorizationService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            authorization_repo: interface.IAuthorizationRepo,
            jwt_secret_key: str,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.authorization_repo = authorization_repo
        self.jwt_secret_key = jwt_secret_key

    @traced_method()
    async def create_tokens(
            self,
            account_id: int,
            account_type: str,
    ) -> model.JWTToken:
        account = (await self.authorization_repo.account_by_id(account_id))[0]

        access_token_payload = {
            "account_id": account_id,
            "account_type": account_type,
            "exp": int(time.time()) + 15 * 60,
        }
        access_token = jwt.encode(access_token_payload, self.jwt_secret_key, algorithm="HS256")

        refresh_token_payload = {
            "account_id": account_id,
            "account_type": account_type,
            "exp": int(time.time()) + 15 * 60,
        }
        refresh_token = jwt.encode(refresh_token_payload, self.jwt_secret_key, algorithm="HS256")

        await self.authorization_repo.update_refresh_token(account.id, refresh_token)

        return model.JWTToken(access_token, refresh_token)

    @traced_method()
    async def check_token(self, token: str) -> model.TokenPayload:
        payload = jwt.decode(
            jwt=token,
            key=self.jwt_secret_key,
            algorithms=["HS256"]
        )

        return model.TokenPayload(
            account_id=int(payload["account_id"]),
            account_type=payload["account_type"],
            exp=int(payload["exp"]),
        )

    @traced_method()
    async def refresh_token(self, refresh_token: str) -> model.JWTToken:
        account = await self.authorization_repo.account_by_refresh_token(refresh_token)
        if not account:
            self.logger.info("Аккаунт не найден по refresh токену")
            raise common.ErrAccountNotFound()

        token_payload = await self.check_token(refresh_token)
        jwt_token = await self.create_tokens(
            token_payload.account_id,
            token_payload.account_type
        )

        return jwt_token
