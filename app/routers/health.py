from fastapi import APIRouter, Query, HTTPException
from app.services.llm import stream_ping

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok", "service": "rcra-dot-compliance-assistant"}

@router.get("/health/meta")
async def health_meta(provider: str = Query("meta", enum=["meta", "fireworks", "baseten"])):
    try:
        return await stream_ping(provider=provider)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"{provider} ping failed: {str(e)}")
