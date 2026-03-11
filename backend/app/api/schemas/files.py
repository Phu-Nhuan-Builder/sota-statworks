from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from app.domain.models.dataset import DatasetMeta, DatasetSession, VariableMeta


class UploadResponse(BaseModel):
    session_id: str
    meta: DatasetMeta
    created_at: str


class SessionInfo(BaseModel):
    session_id: str
    meta: DatasetMeta


class DataPageResponse(BaseModel):
    data: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    n_vars: int


class UpdateMetaRequest(BaseModel):
    variables: Optional[List[VariableMeta]] = None
    file_name: Optional[str] = None
