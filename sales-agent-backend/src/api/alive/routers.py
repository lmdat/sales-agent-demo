from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
from logger import logger


router = APIRouter(
    prefix="/ping"
)

@router.get("/alive")
async def alive(request: Request):
    msg = f"I'm still alive at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    logger.debug(f"Alive: {msg}")
    return JSONResponse(
        content={
            "message": msg
        }, 
        status_code=status.HTTP_200_OK
    )

