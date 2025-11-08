from abc import abstractmethod
from typing import Protocol

from fastapi import UploadFile, Form, Request
from fastapi.responses import JSONResponse

from internal import model
from internal.controller.http.handler.analysis.model import (
    RejectAnalysisBody,
    TakeAnalysisBody,
)


class IAnalysisController(Protocol):
    @abstractmethod
    async def create_analysis(
            self,
            request: Request,
            patient_full_name: str = Form(...),
            analysis_type: str = Form(...),
            study_file: UploadFile = Form(...),
            activity_diary_image: UploadFile | None = Form(None),
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def take_analysis(self, request: Request, body: TakeAnalysisBody) -> JSONResponse:
        pass

    @abstractmethod
    async def reject_analysis(self, request: Request, body: RejectAnalysisBody) -> JSONResponse:
        pass

    @abstractmethod
    async def complete_analysis(
            self,
            request: Request,
            analysis_id: int = Form(...),
            conclusion_file: UploadFile = Form(...)
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def get_all_analyses(self, request: Request,) -> JSONResponse:
        pass

    @abstractmethod
    async def get_analyses_by_nurse(self, request: Request,) -> JSONResponse:
        pass


class IAnalysisService(Protocol):
    @abstractmethod
    async def create_analysis(
            self,
            nurse_id: int,
            patient_full_name: str,
            analysis_type: str,
            study_file: UploadFile,
            activity_diary_image: UploadFile | None,
    ) -> int:
        pass

    @abstractmethod
    async def take_analysis(self, doctor_id: int, analysis_id: int) -> model.Analysis:
        pass

    @abstractmethod
    async def reject_analysis(self, analysis_id: int, rejection_comment: str) -> None:
        pass

    @abstractmethod
    async def complete_analysis(self, analysis_id: int, conclusion_file: UploadFile) -> None:
        pass

    @abstractmethod
    async def get_all_analyses(self) -> list[model.Analysis]:
        pass

    @abstractmethod
    async def get_analyses_by_nurse(self, nurse_id: int) -> list[model.Analysis]:
        pass


class IAnalysisRepo(Protocol):
    @abstractmethod
    async def create_analysis(
            self,
            patient_full_name: str,
            nurse_id: int,
            analysis_type: str,
            study_file_fid: str,
            activity_diary_image_fid: str | None,
    ) -> int:
        pass

    @abstractmethod
    async def get_analysis_by_id(self, analysis_id: int) -> list[model.Analysis]:
        pass

    @abstractmethod
    async def get_all_analyses(self) -> list[model.Analysis]:
        pass

    @abstractmethod
    async def get_analyses_by_nurse(self, nurse_id: int) -> list[model.Analysis]:
        pass

    @abstractmethod
    async def set_doctor_and_start(self, analysis_id: int, doctor_id: int) -> None:
        pass

    @abstractmethod
    async def set_rejection(self, analysis_id: int, rejection_comment: str) -> None:
        pass

    @abstractmethod
    async def set_conclusion(self, analysis_id: int, conclusion_file_fid: str) -> None:
        pass
