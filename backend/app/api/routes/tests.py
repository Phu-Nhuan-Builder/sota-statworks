"""
Hypothesis Tests Routes
"""
import asyncio
import logging
from fastapi import APIRouter

from app.domain.services.spss_io import get_session
from app.domain.services.tests import (
    independent_ttest, paired_ttest, one_sample_ttest, one_way_anova, compute_means
)
from app.api.schemas.tests import TTestRequest, ANOVARequest, MeansRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/ttest/independent")
async def independent_ttest_route(payload: TTestRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        independent_ttest,
        df,
        payload.group_var,
        payload.test_var,
        payload.equal_var,
        payload.alternative,
    )
    return result


@router.post("/ttest/paired")
async def paired_ttest_route(payload: TTestRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        paired_ttest, df, payload.var1, payload.var2
    )
    return result


@router.post("/ttest/one-sample")
async def one_sample_ttest_route(payload: TTestRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        one_sample_ttest, df, payload.variable, payload.test_value or 0.0
    )
    return result


@router.post("/anova/one-way")
async def one_way_anova_route(payload: ANOVARequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        one_way_anova, df, payload.group_var, payload.dep_var, payload.posthoc
    )
    return result


@router.post("/means")
async def means_route(payload: MeansRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        compute_means, df, payload.dep_var, payload.factor_var
    )
    return result
