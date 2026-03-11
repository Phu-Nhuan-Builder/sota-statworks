"""
Descriptives Routes
"""
import asyncio
import logging
from fastapi import APIRouter

from app.domain.services.spss_io import get_session
from app.domain.services.descriptives import (
    compute_frequencies, compute_descriptives, compute_crosstabs, compute_explore
)
from app.api.schemas.descriptives import (
    FrequencyRequest, DescriptivesRequest, CrosstabRequest, ExploreRequest
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/frequencies")
async def frequencies(payload: FrequencyRequest):
    df, meta = get_session(payload.session_id)
    # Get value labels for this variable
    value_labels = {}
    for v in meta.variables:
        if v.name == payload.variable:
            value_labels = v.value_labels or {}
            break

    result = await asyncio.to_thread(
        compute_frequencies, df, payload.variable, value_labels
    )
    return result


@router.post("/descriptives")
async def descriptives(payload: DescriptivesRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        compute_descriptives, df, payload.variables
    )
    return result


@router.post("/crosstabs")
async def crosstabs(payload: CrosstabRequest):
    df, meta = get_session(payload.session_id)
    # Get value labels
    row_vl = {}
    col_vl = {}
    for v in meta.variables:
        if v.name == payload.row_var:
            row_vl = v.value_labels or {}
        if v.name == payload.col_var:
            col_vl = v.value_labels or {}

    result = await asyncio.to_thread(
        compute_crosstabs, df, payload.row_var, payload.col_var, row_vl, col_vl
    )
    return result


@router.post("/explore")
async def explore(payload: ExploreRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        compute_explore, df, payload.variable
    )
    return result
