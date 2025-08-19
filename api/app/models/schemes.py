from pydantic import BaseModel, Field
from typing import Optional, List

# ---- Analyze ----
class AnalyzeIn(BaseModel):
    url: Optional[str] = Field(None, description="Page URL (optional)")
    title: Optional[str] = Field(None, description="Page title (optional)")
    content: str = Field(..., min_length=20, description="Visible page text")

class AnalyzeOut(BaseModel):
    analysis_id: str
    label: str = Field(..., description="credible | unknown | misleading")
    score: float = Field(..., ge=0, le=100, description="0..100")
    tips: List[str]
    model_name: str
    created_at: str

# ---- Feedback ----
class FeedbackIn(BaseModel):
    analysis_id: str
    helpful: bool
    note: Optional[str] = None
    source: str = Field("extension", description="extension | bot")

class FeedbackOut(BaseModel):
    ok: bool

# ---- Share ----
class ShareIn(BaseModel):
    analysis_id: str
    channel: str = Field(..., description="telegram | discord")

class ShareOut(BaseModel):
    token: str
    deep_link_url: str

# ---- Bot ----
class BotCheckIn(BaseModel):
    content: str

class BotCheckOut(BaseModel):
    label: str
    score: float
    tips: List[str]
