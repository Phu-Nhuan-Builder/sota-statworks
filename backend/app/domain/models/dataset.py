from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime


class VariableMeasure(str, Enum):
    nominal = "nominal"
    ordinal = "ordinal"
    scale = "scale"


class VariableType(str, Enum):
    numeric = "numeric"
    string = "string"
    date = "date"


class VariableRole(str, Enum):
    input = "input"
    target = "target"
    both = "both"
    none = "none"
    partition = "partition"
    split = "split"


class ValueLabel(BaseModel):
    value: Union[float, int, str]
    label: str


class VariableMeta(BaseModel):
    name: str
    label: str = ""
    var_type: VariableType = VariableType.numeric
    width: int = 8
    decimals: int = 2
    value_labels: Dict[str, str] = Field(default_factory=dict)
    missing_values: List[Union[float, int, str]] = Field(default_factory=list)
    measure: VariableMeasure = VariableMeasure.scale
    role: VariableRole = VariableRole.input


class DatasetMeta(BaseModel):
    file_name: str
    n_cases: int
    n_vars: int
    variables: List[VariableMeta]
    encoding: str = "utf-8"


class DatasetSession(BaseModel):
    session_id: str
    meta: DatasetMeta
    created_at: datetime = Field(default_factory=datetime.utcnow)
