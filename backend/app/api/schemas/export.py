from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class OutputBlockData(BaseModel):
    id: str
    type: str  # "table" or "chart"
    title: str
    subtitle: Optional[str] = None
    procedure: str
    content: Any


class ExportRequest(BaseModel):
    session_id: str
    format: str  # "pdf" or "excel"
    output_blocks: List[OutputBlockData]
    title: Optional[str] = "Statistical Output"
    include_footer: bool = True
