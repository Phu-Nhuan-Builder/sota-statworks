from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class CorrelationRequest(BaseModel):
    session_id: str
    variables: List[str]
    method: str = "pearson"  # "pearson" or "spearman"
    flag_significance: bool = True


class CorrelationResponse(BaseModel):
    method: str
    variables: List[str]
    r_matrix: List[List[Optional[float]]]
    p_matrix: List[List[Optional[float]]]
    n_matrix: List[List[int]]
    headers: List[str] = []
    rows: List[Any] = []


class RegressionRequest(BaseModel):
    session_id: str
    dependent: str
    independents: List[str]
    method: str = "enter"  # "enter", "stepwise", "forward", "backward"
    include_diagnostics: bool = True


class CoefficientRow(BaseModel):
    variable: str
    B: float
    std_error: float
    beta: Optional[float] = None
    t: float
    pvalue: float
    ci_lower: float
    ci_upper: float
    vif: Optional[float] = None
    tolerance: Optional[float] = None


class RegressionResponse(BaseModel):
    dependent: str
    independents: List[str]
    r: float
    r2: float
    adj_r2: float
    std_error_estimate: float
    f_stat: float
    f_df1: int
    f_df2: int
    f_pvalue: float
    durbin_watson: Optional[float] = None
    anova_table: Dict[str, Any]
    coefficients: List[CoefficientRow]
    condition_indices: Optional[List[float]] = None
    residuals_data: Optional[Dict[str, Any]] = None
    headers: List[str] = []
    rows: List[Any] = []


class LogisticRequest(BaseModel):
    session_id: str
    dependent: str
    independents: List[str]


class LogisticCoefficientRow(BaseModel):
    variable: str
    B: float
    std_error: float
    wald: float
    df: int
    pvalue: float
    exp_B: float
    ci_lower: float
    ci_upper: float


class LogisticResponse(BaseModel):
    dependent: str
    independents: List[str]
    n: int
    neg_2LL: float
    cox_snell_r2: float
    nagelkerke_r2: float
    hosmer_lemeshow_chi2: Optional[float] = None
    hosmer_lemeshow_p: Optional[float] = None
    coefficients: List[LogisticCoefficientRow]
    classification_table: Optional[Dict[str, Any]] = None
    headers: List[str] = []
    rows: List[Any] = []
