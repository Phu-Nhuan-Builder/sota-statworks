"""
Export Routes — PDF and Excel output
"""
import logging
from fastapi import APIRouter
from fastapi.responses import Response

from app.domain.services.export import export_pdf, export_excel
from app.api.schemas.export import ExportRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/pdf")
async def export_pdf_route(payload: ExportRequest):
    """Generate PDF from output blocks. Streams .pdf file."""
    import asyncio
    blocks = [b.model_dump() for b in payload.output_blocks]
    pdf_bytes = await asyncio.to_thread(
        export_pdf, blocks, payload.title or "Statistical Output", payload.include_footer
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=bernie-spss-output.pdf"},
    )


@router.post("/excel")
async def export_excel_route(payload: ExportRequest):
    """Generate Excel (.xlsx) from output blocks."""
    import asyncio
    blocks = [b.model_dump() for b in payload.output_blocks]
    xlsx_bytes = await asyncio.to_thread(
        export_excel, blocks, payload.title or "Statistical Output"
    )
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=bernie-spss-output.xlsx"},
    )
