from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel


class RecodeRule(BaseModel):
    from_value: Union[float, int, str, None]
    to_value: Union[float, int, str, None]


class RecodeRequest(BaseModel):
    source_var: str
    target_var: str  # same as source_var for "into same variable"
    rules: List[RecodeRule]
    else_value: Optional[Union[float, int, str]] = None  # None = keep original


class ComputeRequest(BaseModel):
    target_var: str
    expression: str  # e.g. "var1 + var2 * 2", "log(income)"
    label: Optional[str] = None


class FilterRequest(BaseModel):
    condition: str  # e.g. "age > 18 and gender == 1"
    filter_type: str = "include"  # "include" or "exclude"


class SortRequest(BaseModel):
    sort_keys: List[Dict[str, str]]  # [{"variable": "age", "order": "asc"}, ...]


class RankRequest(BaseModel):
    variables: List[str]
    method: str = "average"  # "average", "min", "max", "first", "dense"
    ascending: bool = True


class TransformResponse(BaseModel):
    session_id: str
    meta: Dict[str, Any]
    n_cases: int
    message: str
