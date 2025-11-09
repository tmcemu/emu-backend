from fastapi import Request, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse

from internal import interface
from internal.controller.http.handler.analysis.model import (
    TakeAnalysisBody,
    RejectAnalysisBody,
)
from pkg.log_wrapper import auto_log
from pkg.trace_wrapper import traced_method


class AnalysisController(interface.IAnalysisController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            analysis_service: interface.IAnalysisService,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.analysis_service = analysis_service

    @auto_log()
    @traced_method()
    async def create_analysis(
            self,
            request: Request,
            analysis_type: str = Form(...),
            study_file: UploadFile = Form(...),
            activity_diary_image: UploadFile | None = Form(None),
    ) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "nurse":
            return JSONResponse(status_code=403, content={"error": "Only nurses can create analyses"})

        analysis_id = await self.analysis_service.create_analysis(
            nurse_id=account_id,
            analysis_type=analysis_type,
            study_file=study_file,
            activity_diary_image=activity_diary_image,
        )

        return JSONResponse(status_code=201, content={"analysis_id": analysis_id})

    @auto_log()
    @traced_method()
    async def take_analysis(self, request: Request, body: TakeAnalysisBody) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "doctor":
            return JSONResponse(status_code=403, content={"error": "Only doctors can take analyses"})

        analysis = await self.analysis_service.take_analysis(
            doctor_id=account_id,
            analysis_id=body.analysis_id,
        )

        return JSONResponse(status_code=200, content=analysis.to_dict())

    @auto_log()
    @traced_method()
    async def reject_analysis(self, request: Request, body: RejectAnalysisBody) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "doctor":
            return JSONResponse(status_code=403, content={"error": "Only doctors can reject analyses"})

        await self.analysis_service.reject_analysis(
            analysis_id=body.analysis_id,
            rejection_comment=body.rejection_comment,
        )

        return JSONResponse(status_code=200, content={"message": "Analysis rejected successfully"})

    @auto_log()
    @traced_method()
    async def complete_analysis(
            self,
            request: Request,
            analysis_id: int = Form(...),
            conclusion_file: UploadFile = Form(...),
    ) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "doctor":
            return JSONResponse(status_code=403, content={"error": "Only doctors can complete analyses"})

        await self.analysis_service.complete_analysis(
            analysis_id=analysis_id,
            conclusion_file=conclusion_file,
        )

        return JSONResponse(status_code=200, content={"message": "Analysis completed successfully"})

    @auto_log()
    @traced_method()
    async def get_all_analyses(self, request: Request) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "doctor":
            return JSONResponse(status_code=403, content={"error": "Only doctors can complete analyses"})

        analyses = await self.analysis_service.get_all_analyses()
        analyses_dict = [analysis.to_dict() for analysis in analyses]

        return JSONResponse(status_code=200, content={"analyses": analyses_dict})

    @auto_log()
    @traced_method()
    async def get_analyses_by_nurse(self, request: Request) -> JSONResponse:
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "nurse":
            return JSONResponse(status_code=403, content={"error": "Only nurses can view their analyses"})

        analyses = await self.analysis_service.get_analyses_by_nurse(nurse_id=account_id)
        analyses_dict = [analysis.to_dict() for analysis in analyses]

        return JSONResponse(status_code=200, content={"analyses": analyses_dict})

    @auto_log()
    @traced_method()
    async def download_study_file(self, request: Request, aid: int):
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "doctor":
            return JSONResponse(status_code=403, content={"error": "Only doctors can download study files"})

        try:
            file_obj, content_type, filename = await self.analysis_service.get_analysis_file(aid, "study")

            return StreamingResponse(
                file_obj,
                media_type=content_type,
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"'
                }
            )
        except Exception as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

    @auto_log()
    @traced_method()
    async def download_activity_diary(self, request: Request, aid: int):
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "doctor":
            return JSONResponse(status_code=403, content={"error": "Only doctors can download activity diary files"})

        try:
            file_obj, content_type, filename = await self.analysis_service.get_analysis_file(aid, "activity_diary")

            return StreamingResponse(
                file_obj,
                media_type=content_type,
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"'
                }
            )
        except Exception as e:
            return JSONResponse(status_code=404, content={"error": str(e)})

    @auto_log()
    @traced_method()
    async def download_conclusion_file(self, request: Request, aid: int):
        authorization_data = request.state.authorization_data
        account_id = authorization_data.account_id
        account_type = authorization_data.account_type

        if account_id == 0:
            return JSONResponse(status_code=403, content={"error": "Unauthorized"})

        if account_type != "nurse":
            return JSONResponse(status_code=403, content={"error": "Only nurses can download conclusion files"})

        try:
            file_obj, content_type, filename = await self.analysis_service.get_analysis_file(aid, "conclusion")

            return StreamingResponse(
                file_obj,
                media_type=content_type,
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"'
                }
            )
        except Exception as e:
            return JSONResponse(status_code=404, content={"error": str(e)})
