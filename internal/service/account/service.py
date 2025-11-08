import bcrypt
import pyotp

from internal import common, interface, model
from pkg.trace_wrapper import traced_method


class AccountService(interface.IAccountService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            account_repo: interface.IAccountRepo,
            emu_authorization_client: interface.IEmuAuthorizationClient,
            password_secret_key: str,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.account_repo = account_repo
        self.emu_authorization_client = emu_authorization_client
        self.password_secret_key = password_secret_key

    @traced_method()
    async def register(self, login: str, password: str, account_type: str) -> model.AuthorizationDataDTO:
        hashed_password = self.__hash_password(password)
        account_id = await self.account_repo.create_account(login, hashed_password, account_type)

        jwt_token = await self.emu_authorization_client.authorization(account_id, account_type)

        return model.AuthorizationDataDTO(
            account_id=account_id,
            account_type=account_type,
            access_token=jwt_token.access_token,
            refresh_token=jwt_token.refresh_token,
        )

    @traced_method()
    async def login(self, login: str, password: str) -> model.AuthorizationDataDTO | None:
        account = await self.account_repo.account_by_login(login)
        if not account:
            self.logger.info("Аккаунт не найден")
            raise common.ErrAccountNotFound()
        account = account[0]

        if not self.__verify_password(account.password, password):
            self.logger.info("Неверный пароль")
            raise common.ErrInvalidPassword()

        jwt_token = await self.emu_authorization_client.authorization(
            account.id, account.account_type
        )

        return model.AuthorizationDataDTO(
            account_id=account.id,
            account_type=account.account_type,
            access_token=jwt_token.access_token,
            refresh_token=jwt_token.refresh_token,
        )

    @traced_method()
    async def change_password(self, account_id: int, new_password: str, old_password: str) -> None:
        account = (await self.account_repo.account_by_id(account_id))[0]

        if not self.__verify_password(account.password, old_password):
            self.logger.info("Неверный старый пароль")
            raise common.ErrInvalidPassword()

        new_hashed_password = self.__hash_password(new_password)
        await self.account_repo.update_password(account_id, new_hashed_password)

    def __verify_password(self, hashed_password: str, password: str) -> bool:
        peppered_password = self.password_secret_key + password
        return bcrypt.checkpw(peppered_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def __verify_two_fa(self, two_fa_code: str, two_fa_key: str) -> bool:
        totp = pyotp.TOTP(two_fa_key)
        return totp.verify(two_fa_code)

    def __hash_password(self, password: str) -> str:
        peppered_password = self.password_secret_key + password
        hashed_password = bcrypt.hashpw(peppered_password.encode("utf-8"), bcrypt.gensalt())

        return hashed_password.decode("utf-8")
