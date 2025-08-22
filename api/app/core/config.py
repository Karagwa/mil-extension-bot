from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    mock_mode: bool = os.getenv("MOCK_MODE", "true").lower() == "false"

    # CORS
    allowed_origins: list[str] = tuple(
        o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
    )

    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    # Bot
    telegram_bot_username: str = os.getenv("TELEGRAM_BOT_USERNAME", "YourMILBot")

settings = Settings()
