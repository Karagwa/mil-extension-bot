from fastapi import APIRouter, HTTPException, Request
from app.models.schemes import ShareIn, ShareOut
from app.core.config import settings
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/", response_model=ShareOut)
def share(request: Request, payload: ShareIn):
    db = request.app.state.db

    # Ensure analysis exists
    res = db.table("analyses").select("*").eq("id", payload.analysis_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="analysis_id not found")

    token = str(uuid4())
    if payload.channel == "telegram":
        deep_link = f"https://t.me/{settings.telegram_bot_username}?start={token}"
    elif payload.channel == "discord":
        # For Discord, you'd handle differently (e.g., slash command). Placeholder:
        deep_link = f"https://discord.com/app?mil_token={token}"
    else:
        raise HTTPException(status_code=400, detail="channel must be telegram or discord")

    row = {
        "id": str(uuid4()),
        "analysis_id": payload.analysis_id,
        "channel": payload.channel,
        "token": token,
        "deep_link_url": deep_link,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=3)).isoformat(),
    }
    result_obj = db.table("shares").insert(row)
    if hasattr(result_obj, "execute") and callable(result_obj.execute):
        result_obj.execute()
    return ShareOut(token=token, deep_link_url=deep_link)
