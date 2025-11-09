import io

from fastapi import UploadFile

from internal import common, interface, model
from pkg.trace_wrapper import traced_method


class AnalysisService(interface.IAnalysisService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            analysis_repo: interface.IAnalysisRepo,
            storage: interface.IStorage,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.analysis_repo = analysis_repo
        self.storage = storage

    @traced_method()
    async def create_analysis(
            self,
            nurse_id: int,
            analysis_type: str,
            study_file: UploadFile,
            activity_diary_image: UploadFile | None,
    ) -> int:
        study_file_content = await study_file.read()
        study_file_bytes = io.BytesIO(study_file_content)
        study_file_original_name = study_file.filename or "study_file"
        study_file_result = await self.storage.upload(study_file_bytes, study_file_original_name)
        study_file_fid = study_file_result.fid

        activity_diary_fid = None
        activity_diary_original_name = None
        if activity_diary_image:
            diary_content = await activity_diary_image.read()
            diary_bytes = io.BytesIO(diary_content)
            activity_diary_original_name = activity_diary_image.filename or "activity_diary"
            diary_result = await self.storage.upload(diary_bytes, activity_diary_original_name)
            activity_diary_fid = diary_result.fid

        analysis_id = await self.analysis_repo.create_analysis(
            nurse_id=nurse_id,
            analysis_type=analysis_type,
            study_file_fid=study_file_fid,
            study_file_original_name=study_file_original_name,
            activity_diary_image_fid=activity_diary_fid,
            activity_diary_original_name=activity_diary_original_name,
        )

        return analysis_id

    @traced_method()
    async def take_analysis(self, doctor_id: int, analysis_id: int) -> model.Analysis:
        analyses = await self.analysis_repo.get_analysis_by_id(analysis_id)
        if not analyses:
            raise common.ErrAnalysisNotFound()

        analysis = analyses[0]

        if analysis.status != "pending":
            raise common.ErrAnalysisInvalidStatus()

        await self.analysis_repo.set_doctor_and_start(analysis_id, doctor_id)

        updated_analyses = await self.analysis_repo.get_analysis_by_id(analysis_id)
        return updated_analyses[0]

    @traced_method()
    async def reject_analysis(self, analysis_id: int, rejection_comment: str) -> None:
        analyses = await self.analysis_repo.get_analysis_by_id(analysis_id)
        if not analyses:
            raise common.ErrAnalysisNotFound()

        analysis = analyses[0]

        if analysis.status != "in_work":
            raise common.ErrAnalysisInvalidStatus()

        await self.analysis_repo.set_rejection(analysis_id, rejection_comment)

    @traced_method()
    async def complete_analysis(self, analysis_id: int, conclusion_file: UploadFile) -> None:
        analyses = await self.analysis_repo.get_analysis_by_id(analysis_id)
        if not analyses:
            raise common.ErrAnalysisNotFound()

        analysis = analyses[0]

        if analysis.status != "in_work":
            raise common.ErrAnalysisInvalidStatus()

        conclusion_content = await conclusion_file.read()
        conclusion_bytes = io.BytesIO(conclusion_content)
        conclusion_original_name = conclusion_file.filename or "conclusion"
        conclusion_result = await self.storage.upload(conclusion_bytes, conclusion_original_name)
        conclusion_fid = conclusion_result.fid

        await self.analysis_repo.set_conclusion(analysis_id, conclusion_fid, conclusion_original_name)

    @traced_method()
    async def get_all_analyses(self) -> list[model.Analysis]:
        analyses = await self.analysis_repo.get_all_analyses()
        return analyses

    @traced_method()
    async def get_analyses_by_nurse(self, nurse_id: int) -> list[model.Analysis]:
        analyses = await self.analysis_repo.get_analyses_by_nurse(nurse_id)
        return analyses

    @traced_method()
    async def get_analysis_file(self, analysis_id: int, file_type: str) -> tuple[io.BytesIO, str, str]:
        analyses = await self.analysis_repo.get_analysis_by_id(analysis_id)
        if not analyses:
            raise common.ErrAnalysisNotFound()

        analysis = analyses[0]

        # Определяем FID в зависимости от типа файла
        if file_type == "study":
            fid = analysis.study_file_fid
            filename = analysis.study_file_original_name
        elif file_type == "activity_diary":
            fid = analysis.activity_diary_image_fid
            filename = analysis.activity_diary_original_name
        elif file_type == "conclusion":
            fid = analysis.conclusion_file_fid
            filename = analysis.conclusion_file_original_name
        else:
            raise ValueError(f"Invalid file type: {file_type}")

        if not fid:
            raise common.ErrAnalysisNotFound()

        # Скачиваем файл из storage
        file_obj, content_type = await self.storage.download(fid, filename)

        return file_obj, content_type, filename
