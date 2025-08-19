from fastapi import APIRouter, HTTPException, Request
from app.models.schemes import AnalyzeIn, AnalyzeOut
from app.services.mil_analyzer import Analyzer
from uuid import uuid4
from datetime import datetime

router = APIRouter()
_analyzer = Analyzer()  # load once

@router.post("/", response_model=AnalyzeOut)
def analyze(request: Request, payload: AnalyzeIn):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Content is required")

    result = _analyzer.analyze(payload.content)
    analysis_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()

    row = {
        "id": analysis_id,
        "url": payload.url,
        "title": payload.title,
        "raw_text": payload.content,
        "label": result["label"],
        "score": result["score"],
        "tips": result["tips"],
        "model_name": result["model_name"],
        "created_at": created_at,
    }

    db = request.app.state.db
    result_obj = db.table("analyses").insert(row)
    # Only call .execute() if the method exists (Supabase), otherwise skip (in-memory)
    if hasattr(result_obj, "execute") and callable(result_obj.execute):
        result_obj.execute()

    return AnalyzeOut(
        analysis_id=analysis_id,
        label=result["label"],
        score=result["score"],
        tips=result["tips"],
        model_name=result["model_name"],
        created_at=created_at,
    )
