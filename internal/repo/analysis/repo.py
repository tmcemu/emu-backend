from internal import interface, model
from pkg.trace_wrapper import traced_method

from .sql_query import *


class AnalysisRepo(interface.IAnalysisRepo):
    def __init__(
        self,
        tel: interface.ITelemetry,
        db: interface.IDB,
    ):
        self.tracer = tel.tracer()
        self.db = db

    @traced_method()
    async def create_analysis(
        self,
        nurse_id: int,
        analysis_type: str,
        study_file_fid: str,
        activity_diary_image_fid: str | None,
    ) -> int:
        args = {
            "nurse_id": nurse_id,
            "analysis_type": analysis_type,
            "study_file_fid": study_file_fid,
            "activity_diary_image_fid": activity_diary_image_fid or "",
        }

        analysis_id = await self.db.insert(create_analysis, args)
        return analysis_id

    @traced_method()
    async def get_analysis_by_id(self, analysis_id: int) -> list[model.Analysis]:
        args = {"analysis_id": analysis_id}
        rows = await self.db.select(get_analysis_by_id, args)
        analyses = model.Analysis.serialize(rows) if rows else []
        return analyses

    @traced_method()
    async def get_all_analyses(self) -> list[model.Analysis]:
        args = {}
        rows = await self.db.select(get_all_analyses, args)
        analyses = model.Analysis.serialize(rows) if rows else []
        return analyses

    @traced_method()
    async def get_analyses_by_nurse(self, nurse_id: int) -> list[model.Analysis]:
        args = {"nurse_id": nurse_id}
        rows = await self.db.select(get_analyses_by_nurse, args)
        analyses = model.Analysis.serialize(rows) if rows else []
        return analyses

    @traced_method()
    async def set_doctor_and_start(self, analysis_id: int, doctor_id: int) -> None:
        args = {
            "analysis_id": analysis_id,
            "doctor_id": doctor_id,
        }
        await self.db.update(set_doctor_and_start, args)

    @traced_method()
    async def set_rejection(self, analysis_id: int, rejection_comment: str) -> None:
        args = {
            "analysis_id": analysis_id,
            "rejection_comment": rejection_comment,
        }
        await self.db.update(set_rejection, args)

    @traced_method()
    async def set_conclusion(self, analysis_id: int, conclusion_file_fid: str) -> None:
        args = {
            "analysis_id": analysis_id,
            "conclusion_file_fid": conclusion_file_fid,
        }
        await self.db.update(set_conclusion, args)
