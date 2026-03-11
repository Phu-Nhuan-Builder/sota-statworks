from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class FactorRequest(BaseModel):
    session_id: str
    variables: List[str]
    n_factors: int = 3
    extraction: str = "principal"  # "principal", "minres", "ml"
    rotation: str = "varimax"  # "varimax", "oblimin", "quartimax", "promax", "none"


class FactorResponse(BaseModel):
    variables: List[str]
    n_factors: int
    extraction: str
    rotation: str
    loadings: List[List[float]]  # n_vars × n_factors
    communalities: List[float]
    eigenvalues: List[float]
    explained_variance: List[float]
    cumulative_variance: List[float]
    kmo: float
    bartlett_chi2: float
    bartlett_df: int
    bartlett_p: float
    scree_data: List[float]
    headers: List[str] = []
    rows: List[Any] = []


class ReliabilityRequest(BaseModel):
    session_id: str
    variables: List[str]


class ItemStats(BaseModel):
    variable: str
    mean: float
    std: float
    item_total_corr: float
    alpha_if_deleted: float


class ReliabilityResponse(BaseModel):
    variables: List[str]
    n_items: int
    n_cases: int
    cronbach_alpha: float
    cronbach_alpha_ci_lower: float
    cronbach_alpha_ci_upper: float
    item_stats: List[ItemStats]
    headers: List[str] = []
    rows: List[Any] = []
