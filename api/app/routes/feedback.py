from fastapi import APIRouter, Request
from app.models.schemes import FeedbackIn, FeedbackOut
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=FeedbackOut)
def feedback(request: Request, payload: FeedbackIn):
    row = {
        "id": str(uuid4()),
        "analysis_id": payload.analysis_id,
        "helpful": payload.helpful,
        "note": payload.note,
        "source": payload.source,
        "created_at": datetime.utcnow().isoformat(),
    }
    db = request.app.state.db
    result_obj = db.table("feedback").insert(row)
    if hasattr(result_obj, "execute") and callable(result_obj.execute):
        result_obj.execute()
    return FeedbackOut(ok=True)
