"""
Factor Analysis & Reliability Routes
"""
import asyncio
import logging
from fastapi import APIRouter

from app.domain.services.spss_io import get_session
from app.domain.services.factor_analysis import run_efa, run_reliability
from app.api.schemas.factor import FactorRequest, ReliabilityRequest
from app.domain.models.job import JobStatus, JobResult

logger = logging.getLogger(__name__)
router = APIRouter()

# Threshold: n_vars × n_cases > 50,000 → use Celery
CELERY_THRESHOLD = 50_000


@router.post("/efa")
async def efa_route(payload: FactorRequest):
    df, meta = get_session(payload.session_id)
    n_vars = len(payload.variables)
    n_cases = len(df)

    if n_vars * n_cases > CELERY_THRESHOLD:
        # Use Celery for large datasets
        try:
            from app.tasks.celery_tasks import run_factor_analysis_task
            task = run_factor_analysis_task.apply_async(args=[
                payload.session_id,
                payload.variables,
                payload.n_factors,
                payload.extraction,
                payload.rotation,
            ])
            return {"job_id": task.id, "status": "PENDING", "message": "Factor analysis queued"}
        except Exception as e:
            logger.warning(f"Celery unavailable, falling back to thread: {e}")

    # For small datasets or if Celery unavailable: asyncio.to_thread
    result = await asyncio.to_thread(
        run_efa, df, payload.variables, payload.n_factors,
        payload.extraction, payload.rotation
    )
    return result


@router.get("/efa/{job_id}")
async def efa_job_status(job_id: str):
    """Poll Celery task status."""
    try:
        from app.tasks.celery_tasks import celery_app
        from celery.result import AsyncResult
        task = AsyncResult(job_id, app=celery_app)
        result = None
        error = None
        progress_msg = None

        if task.state == "SUCCESS":
            result = task.result
        elif task.state == "FAILURE":
            error = str(task.result)
        elif task.state == "PROGRESS":
            progress_msg = task.info.get("step", "") if task.info else None

        return JobResult(
            job_id=job_id,
            status=JobStatus(task.state) if task.state in JobStatus._value2member_map_ else JobStatus.PENDING,
            progress_msg=progress_msg,
            result=result,
            error=error,
        )
    except Exception as e:
        return {"job_id": job_id, "status": "UNKNOWN", "error": str(e)}


@router.post("/reliability")
async def reliability_route(payload: ReliabilityRequest):
    df, meta = get_session(payload.session_id)
    result = await asyncio.to_thread(
        run_reliability, df, payload.variables
    )
    return result
