from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging

from .webhook_handler import admission_review_response

router = APIRouter()
logger = logging.getLogger("admission_router")

@router.post("/validate")
async def validate(request: Request):
    body = await request.json()
    resp = admission_review_response(body)
    return JSONResponse(content=resp, status_code=200)
