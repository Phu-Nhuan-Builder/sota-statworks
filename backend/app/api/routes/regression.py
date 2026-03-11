"""
Regression & Correlation Routes
"""
import asyncio
import logging
from fastapi import APIRouter

from app.domain.services.spss_io import get_session
from app.domain.services.regression import (
    pearson_spearman_correlation, ols_regression, binary_logistic
)
from app.api.schemas.regression import CorrelationRequest, RegressionRequest, LogisticRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/correlation")
async def correlation_route(payload: CorrelationRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        pearson_spearman_correlation, df, payload.variables, payload.method
    )
    return result


@router.post("/linear")
async def linear_regression_route(payload: RegressionRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        ols_regression, df, payload.dependent, payload.independents,
        payload.method, payload.include_diagnostics
    )
    return result


@router.post("/logistic/binary")
async def logistic_binary_route(payload: LogisticRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        binary_logistic, df, payload.dependent, payload.independents
    )
    return result
