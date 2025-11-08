from fastapi import FastAPI

from internal import interface, model


def NewHTTP(
    db: interface.IDB,
    account_controller: interface.IAccountController,
    authorization_controller: interface.IAuthorizationController,
    analysis_controller: interface.IAnalysisController,
    http_middleware: interface.IHttpMiddleware,
    prefix: str,
):
    app = FastAPI(
        openapi_url=prefix + "/openapi.json",
        docs_url=prefix + "/docs",
        redoc_url=prefix + "/redoc",
    )
    include_middleware(app, http_middleware)
    include_db_handler(app, db, prefix)

    include_account_handlers(app, account_controller, prefix)
    include_authorization_handlers(app, authorization_controller, prefix)
    include_analysis_handlers(app, analysis_controller, prefix)

    return app


def include_middleware(
    app: FastAPI,
    http_middleware: interface.IHttpMiddleware,
):
    http_middleware.authorization_middleware03(app)
    http_middleware.logger_middleware02(app)
    http_middleware.trace_middleware01(app)


def include_account_handlers(app: FastAPI, account_controller: interface.IAccountController, prefix: str):
    # Регистрация пользователя
    app.add_api_route(
        prefix + "/register",
        account_controller.register,
        methods=["POST"],
        tags=["Account"],
    )

    # Вход пользователя
    app.add_api_route(
        prefix + "/login",
        account_controller.login,
        methods=["POST"],
        tags=["Account"],
    )

    # Изменение пароля
    app.add_api_route(
        prefix + "/password/change",
        account_controller.change_password,
        methods=["PUT"],
        tags=["Account"],
    )


def include_authorization_handlers(
    app: FastAPI, authorization_controller: interface.IAuthorizationController, prefix: str
):
    # Создание токенов авторизации
    app.add_api_route(
        prefix + "/authorization",
        authorization_controller.authorization,
        methods=["POST"],
        tags=["Authorization"],
    )

    # Проверка токена авторизации
    app.add_api_route(
        prefix + "/check-authorization",
        authorization_controller.check_authorization,
        methods=["GET"],
        tags=["Authorization"],
    )

    # Обновление токена
    app.add_api_route(
        prefix + "/refresh-token",
        authorization_controller.refresh_token,
        methods=["POST"],
        tags=["Authorization"],
    )


def include_analysis_handlers(
    app: FastAPI, analysis_controller: interface.IAnalysisController, prefix: str
):
    # Создание анализа (медсестры)
    app.add_api_route(
        prefix + "/analysis/create",
        analysis_controller.create_analysis,
        methods=["POST"],
        tags=["Analysis"],
    )

    # Взять анализ на рассмотрение (врачи)
    app.add_api_route(
        prefix + "/analysis/take",
        analysis_controller.take_analysis,
        methods=["POST"],
        tags=["Analysis"],
    )

    # Отклонить анализ (врачи)
    app.add_api_route(
        prefix + "/analysis/reject",
        analysis_controller.reject_analysis,
        methods=["POST"],
        tags=["Analysis"],
    )

    # Завершить анализ (врачи)
    app.add_api_route(
        prefix + "/analysis/complete",
        analysis_controller.complete_analysis,
        methods=["POST"],
        tags=["Analysis"],
    )

    # Получить все анализы (врачи)
    app.add_api_route(
        prefix + "/analysis/all",
        analysis_controller.get_all_analyses,
        methods=["GET"],
        tags=["Analysis"],
    )

    # Получить анализы медсестры (медсестры)
    app.add_api_route(
        prefix + "/analysis/nurse",
        analysis_controller.get_analyses_by_nurse,
        methods=["GET"],
        tags=["Analysis"],
    )


def include_db_handler(app: FastAPI, db: interface.IDB, prefix: str):
    app.add_api_route(prefix + "/table/create", create_table_handler(db), methods=["GET"])
    app.add_api_route(prefix + "/table/drop", drop_table_handler(db), methods=["GET"])
    app.add_api_route(prefix + "/health", heath_check_handler(), methods=["GET"])


def heath_check_handler():
    async def heath_check():
        return "ok"

    return heath_check


def create_table_handler(db: interface.IDB):
    async def create_table():
        try:
            await db.multi_query(model.create_tables_queries)
        except Exception as err:
            raise err

    return create_table


def drop_table_handler(db: interface.IDB):
    async def drop_table():
        try:
            await db.multi_query(model.drop_queries)
        except Exception as err:
            raise err

    return drop_table
