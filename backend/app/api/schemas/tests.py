from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class TTestRequest(BaseModel):
    session_id: str
    group_var: Optional[str] = None  # for independent
    test_var: Optional[str] = None
    var1: Optional[str] = None  # for paired
    var2: Optional[str] = None  # for paired
    variable: Optional[str] = None  # for one-sample
    test_value: Optional[float] = 0.0  # for one-sample
    equal_var: bool = True
    alternative: str = "two-sided"  # "two-sided", "less", "greater"


class GroupStats(BaseModel):
    group: Any
    n: int
    mean: float
    std: float
    se: float


class TTestResponse(BaseModel):
    test_type: str
    statistic: float
    df: float
    pvalue: float
    mean_diff: Optional[float] = None
    cohen_d: Optional[float] = None
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    levene_F: Optional[float] = None
    levene_p: Optional[float] = None
    group_stats: Optional[List[GroupStats]] = None
    headers: List[str] = []
    rows: List[Any] = []


class ANOVARequest(BaseModel):
    session_id: str
    group_var: str
    dep_var: str
    posthoc: str = "tukey"  # "tukey", "bonferroni", "scheffe"


class ANOVAResponse(BaseModel):
    dep_var: str
    group_var: str
    f_statistic: float
    df_between: int
    df_within: int
    p_value: float
    eta_squared: float
    levene_F: Optional[float] = None
    levene_p: Optional[float] = None
    group_stats: List[Dict[str, Any]]
    posthoc_results: Optional[List[Dict[str, Any]]] = None
    anova_table: Dict[str, Any]
    headers: List[str] = []
    rows: List[Any] = []


class MeansRequest(BaseModel):
    session_id: str
    dep_var: str
    factor_var: str


class MeansResponse(BaseModel):
    dep_var: str
    factor_var: str
    group_means: List[Dict[str, Any]]
    anova_table: Optional[Dict[str, Any]] = None
    headers: List[str] = []
    rows: List[Any] = []
