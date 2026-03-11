"""
Data Transform Routes
All transform operations update SESSION_STORE in-place.
"""
import asyncio
import logging
from fastapi import APIRouter

from app.domain.services.spss_io import get_session, update_session
from app.domain.services.transforms import (
    recode_variable, compute_variable, select_cases, sort_cases, rank_cases
)
from app.api.schemas.transform import (
    RecodeRequest, ComputeRequest, FilterRequest, SortRequest, RankRequest, TransformResponse
)
from app.domain.models.dataset import VariableMeta, VariableType, VariableMeasure, VariableRole

logger = logging.getLogger(__name__)
router = APIRouter()


def _update_meta_for_new_var(meta, var_name: str, label: str = "") -> None:
    """Add a new variable to metadata if it doesn't exist."""
    existing_names = [v.name for v in meta.variables]
    if var_name not in existing_names:
        meta.variables.append(VariableMeta(
            name=var_name,
            label=label,
            var_type=VariableType.numeric,
            width=8,
            decimals=2,
            value_labels={},
            missing_values=[],
            measure=VariableMeasure.scale,
            role=VariableRole.input,
        ))


@router.post("/{session_id}/recode", response_model=TransformResponse)
async def recode(session_id: str, payload: RecodeRequest):
    df, meta = get_session(session_id)

    df_new = await asyncio.to_thread(
        recode_variable,
        df,
        payload.source_var,
        payload.target_var,
        [r.model_dump() for r in payload.rules],
        payload.else_value,
    )

    # Update meta if new variable
    _update_meta_for_new_var(meta, payload.target_var)
    meta = meta.model_copy(update={"n_vars": len(df_new.columns), "n_cases": len(df_new)})
    update_session(session_id, df_new, meta)

    return TransformResponse(
        session_id=session_id,
        meta=meta.model_dump(),
        n_cases=len(df_new),
        message=f"Recoded '{payload.source_var}' → '{payload.target_var}'",
    )


@router.post("/{session_id}/compute", response_model=TransformResponse)
async def compute(session_id: str, payload: ComputeRequest):
    df, meta = get_session(session_id)

    df_new = await asyncio.to_thread(
        compute_variable,
        df,
        payload.target_var,
        payload.expression,
        payload.label,
    )

    _update_meta_for_new_var(meta, payload.target_var, payload.label or "")
    meta = meta.model_copy(update={"n_vars": len(df_new.columns), "n_cases": len(df_new)})
    update_session(session_id, df_new, meta)

    return TransformResponse(
        session_id=session_id,
        meta=meta.model_dump(),
        n_cases=len(df_new),
        message=f"Computed variable '{payload.target_var}'",
    )


@router.post("/{session_id}/filter", response_model=TransformResponse)
async def filter_cases(session_id: str, payload: FilterRequest):
    df, meta = get_session(session_id)

    df_new = await asyncio.to_thread(
        select_cases, df, payload.condition, payload.filter_type
    )

    meta = meta.model_copy(update={"n_cases": len(df_new)})
    update_session(session_id, df_new, meta)

    return TransformResponse(
        session_id=session_id,
        meta=meta.model_dump(),
        n_cases=len(df_new),
        message=f"Filtered: {len(df) - len(df_new)} rows removed",
    )


@router.post("/{session_id}/sort", response_model=TransformResponse)
async def sort(session_id: str, payload: SortRequest):
    df, meta = get_session(session_id)

    df_new = await asyncio.to_thread(
        sort_cases, df, payload.sort_keys
    )

    update_session(session_id, df_new, meta)

    return TransformResponse(
        session_id=session_id,
        meta=meta.model_dump(),
        n_cases=len(df_new),
        message="Data sorted",
    )


@router.post("/{session_id}/rank", response_model=TransformResponse)
async def rank(session_id: str, payload: RankRequest):
    df, meta = get_session(session_id)

    df_new = await asyncio.to_thread(
        rank_cases, df, payload.variables, payload.method, payload.ascending
    )

    # Register any new RANK_ columns in metadata
    for var in payload.variables:
        if var in df.columns:
            _update_meta_for_new_var(meta, f"RANK_{var}", label=f"Rank of {var}")

    meta = meta.model_copy(update={"n_vars": len(df_new.columns), "n_cases": len(df_new)})
    update_session(session_id, df_new, meta)

    return TransformResponse(
        session_id=session_id,
        meta=meta.model_dump(),
        n_cases=len(df_new),
        message=f"Ranked {len(payload.variables)} variable(s)",
    )
