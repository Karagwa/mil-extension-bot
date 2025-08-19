from fastapi import APIRouter, HTTPException, Request
from app.models.schemes import BotCheckIn, BotCheckOut
from app.services.mil_analyzer import Analyzer

router = APIRouter()
_analyzer = Analyzer()

@router.post("/check", response_model=BotCheckOut)
def bot_check(_: Request, payload: BotCheckIn):
    result = _analyzer.analyze(payload.content)
    return BotCheckOut(label=result["label"], score=result["score"], tips=result["tips"])

@router.get("/resolve/{token}")
def resolve_share(request: Request, token: str):
    """
    Bots call this after deep-link: /resolve/<token> → analysis row.
    """
    db = request.app.state.db
    sres = db.table("shares").select("*").eq("token", token).execute()
    if not sres.data:
        raise HTTPException(status_code=404, detail="token not found")

    analysis_id = sres.data[0]["analysis_id"]
    ares = db.table("analyses").select("*").eq("id", analysis_id).execute()
    if not ares.data:
        raise HTTPException(status_code=404, detail="analysis missing")

    row = ares.data[0]
    # Return minimal fields a bot would render
    return {
        "analysis_id": row["id"],
        "url": row.get("url"),
        "title": row.get("title"),
        "label": row["label"],
        "score": row["score"],
        "tips": row["tips"],
        "created_at": row["created_at"],
    }
