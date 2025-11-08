from dataclasses import dataclass
from datetime import datetime


@dataclass
class Account:
    id: int

    login: str
    password: str
    refresh_token: str

    account_type: str # doctor, nurse

    created_at: datetime

    @classmethod
    def serialize(cls, rows) -> list["Account"]:
        return [
            cls(
                id=row.id,
                login=row.login,
                password=row.password,
                refresh_token=row.refresh_token,
                account_type=row.account_type,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "login": self.login,
            "password": self.password,
            "refresh_token": self.refresh_token,
            "account_type": self.account_type,
            "created_at": self.created_at.isoformat(),
        }

