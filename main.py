from contextvars import ContextVar

import uvicorn

from infrastructure.pg.pg import PG
from infrastructure.telemetry.telemetry import AlertManager, Telemetry
from infrastructure.weedfs.weedfs import AsyncWeed
from internal.app.http.app import NewHTTP
from internal.config.config import Config
from internal.controller.http.handler.account.handler import AccountController
from internal.controller.http.handler.analysis.handler import AnalysisController
from internal.controller.http.handler.authorization.handler import AuthorizationController
from internal.controller.http.middlerware.middleware import HttpMiddleware
from internal.repo.account.repo import AccountRepo
from internal.repo.analysis.repo import AnalysisRepo
from internal.repo.authorization.repo import AuthorizationRepo
from internal.service.account.service import AccountService
from internal.service.analysis.service import AnalysisService
from internal.service.authorization.service import AuthorizationService
from pkg.client.internal.emu_authorization.client import EmuAuthorizationClient

cfg = Config()

log_context: ContextVar[dict] = ContextVar("log_context", default={})

alert_manager = AlertManager(
    cfg.alert_tg_bot_token,
    cfg.service_name,
    cfg.alert_tg_chat_id,
    cfg.alert_tg_chat_thread_id,
    cfg.grafana_url,
    cfg.monitoring_redis_host,
    cfg.monitoring_redis_port,
    cfg.monitoring_redis_db,
    cfg.monitoring_redis_password,
)

tel = Telemetry(
    cfg.log_level,
    cfg.root_path,
    cfg.environment,
    cfg.service_name,
    cfg.service_version,
    cfg.otlp_host,
    cfg.otlp_port,
    log_context,
    alert_manager,
)

# Инициализация клиентов
db = PG(tel, cfg.db_user, cfg.db_pass, cfg.db_host, cfg.db_port, cfg.db_name)

emu_authorization_client = EmuAuthorizationClient(
    tel=tel,
    host=cfg.emu_authorization_host,
    port=cfg.emu_authorization_port,
    log_context=log_context,
)

storage = AsyncWeed(cfg.weedfs_host, cfg.weedfs_port)

# Инициализация репозиториев
account_repo = AccountRepo(tel, db)
authorization_repo = AuthorizationRepo(tel, db)
analysis_repo = AnalysisRepo(tel, db)

# Инициализация сервисов
account_service = AccountService(
    tel=tel,
    account_repo=account_repo,
    emu_authorization_client=emu_authorization_client,
    password_secret_key=cfg.password_secret_key,
)

authorization_service = AuthorizationService(
    tel=tel,
    authorization_repo=authorization_repo,
    jwt_secret_key=cfg.jwt_secret_key,
)

analysis_service = AnalysisService(
    tel=tel,
    analysis_repo=analysis_repo,
    storage=storage,
)

# Инициализация контроллеров
account_controller = AccountController(tel, account_service, cfg.interserver_secret_key)
authorization_controller = AuthorizationController(tel, authorization_service, cfg.prefix)
analysis_controller = AnalysisController(tel, analysis_service)

# Инициализация middleware
http_middleware = HttpMiddleware(tel, emu_authorization_client, cfg.prefix, log_context)

app = NewHTTP(
    db=db,
    account_controller=account_controller,
    authorization_controller=authorization_controller,
    analysis_controller=analysis_controller,
    http_middleware=http_middleware,
    prefix=cfg.prefix,
)

if __name__ == "__main__":
    if cfg.environment == "prod":
        workers = 1
    else:
        workers = 1

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(cfg.http_port),
        workers=workers,
        loop="uvloop",
        access_log=False,
    )
