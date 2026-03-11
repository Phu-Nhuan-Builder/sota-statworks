import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bernie-SPSS API",
    description="Open-source web-based statistical software for Vietnamese economics students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Routers — import lazily to avoid circular imports
from app.api.routes import files as files_router
from app.api.routes import descriptives as descriptives_router
from app.api.routes import tests as tests_router
from app.api.routes import regression as regression_router
from app.api.routes import factor as factor_router
from app.api.routes import transforms as transforms_router
from app.api.routes import jobs as jobs_router
from app.api.routes import export as export_router

app.include_router(files_router.router, prefix="/files", tags=["File I/O"])
app.include_router(descriptives_router.router, prefix="/descriptives", tags=["Descriptives"])
app.include_router(tests_router.router, prefix="/tests", tags=["Hypothesis Tests"])
app.include_router(regression_router.router, prefix="/regression", tags=["Regression"])
app.include_router(factor_router.router, prefix="/factor", tags=["Factor & Reliability"])
app.include_router(transforms_router.router, prefix="/transform", tags=["Data Transform"])
app.include_router(jobs_router.router, prefix="/jobs", tags=["Async Jobs"])
app.include_router(export_router.router, prefix="/export", tags=["Export"])


@app.get("/health", tags=["Health"])
async def health():
    from app.domain.services.spss_io import SESSION_STORE
    return {"status": "ok", "sessions": len(SESSION_STORE), "environment": settings.ENVIRONMENT}


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bernie-SPSS API", "docs": "/docs"}
