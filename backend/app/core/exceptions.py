from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Any


class StatisticalError(Exception):
    def __init__(self, code: str, message: str, details: Any = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class SessionNotFoundError(Exception):
    def __init__(self, session_id: str):
        self.session_id = session_id
        super().__init__(f"Session not found: {session_id}")


class FileFormatError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StatisticalError)
    async def statistical_error_handler(request: Request, exc: StatisticalError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "STATISTICAL_ERROR",
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_handler(request: Request, exc: SessionNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "error": "SESSION_NOT_FOUND",
                "message": str(exc),
                "session_id": exc.session_id,
            },
        )

    @app.exception_handler(FileFormatError)
    async def file_format_error_handler(request: Request, exc: FileFormatError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "FILE_FORMAT_ERROR",
                "message": str(exc),
            },
        )
