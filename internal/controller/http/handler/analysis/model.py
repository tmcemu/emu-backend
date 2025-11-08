from pydantic import BaseModel


class TakeAnalysisBody(BaseModel):
    analysis_id: int


class RejectAnalysisBody(BaseModel):
    analysis_id: int
    rejection_comment: str