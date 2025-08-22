from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.db import get_db
from app.routes import analyze, feedback, share, bot

app = FastAPI(
    title="MIL Browser Extension API",
    description="Detection + MIL education + bot handoff",
    version="1.0.0",
)

# CORS for extension & bot
if settings.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Attach a DB-like client (Supabase or in-memory)
app.state.db = get_db()

# Routers
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])  #
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(share.router,    prefix="/share",    tags=["Share"])
app.include_router(bot.router,      prefix="/bot",      tags=["Bot"])

@app.get("/", tags=["Health"])
def health():
    return {"ok": True, "env": settings.app_env, "mock": settings.mock_mode}
