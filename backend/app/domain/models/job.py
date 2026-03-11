from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROGRESS = "PROGRESS"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class JobResult(BaseModel):
    job_id: str
    status: JobStatus
    progress_msg: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
