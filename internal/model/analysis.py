from dataclasses import dataclass
from datetime import datetime


@dataclass
class Analysis:
    id: int

    nurse_id: int
    doctor_id: int

    analysis_type: str
    study_file_fid: str
    activity_diary_image_fid: str
    status: str
    conclusion_file_fid: str
    rejection_comment: str

    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def serialize(cls, rows) -> list["Analysis"]:
        return [
            cls(
                id=row.id,
                nurse_id=row.nurse_id,
                doctor_id=row.doctor_id,
                analysis_type=row.analysis_type,
                study_file_fid=row.study_file_fid,
                activity_diary_image_fid=row.activity_diary_image_fid,
                status=row.status,
                conclusion_file_fid=row.conclusion_file_fid,
                rejection_comment=row.rejection_comment,
                started_at=row.started_at,
                finished_at=row.finished_at,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nurse_id": self.nurse_id,
            "doctor_id": self.doctor_id,
            "analysis_type": self.analysis_type,
            "study_file_fid": self.study_file_fid,
            "activity_diary_image_fid": self.activity_diary_image_fid,
            "status": self.status,
            "conclusion_file_fid": self.conclusion_file_fid,
            "rejection_comment": self.rejection_comment,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

