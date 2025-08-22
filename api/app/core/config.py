# from dataclasses import dataclass
# import os
# from dotenv import load_dotenv

# load_dotenv()

# @dataclass
# class Settings:
#     app_env: str = os.getenv("APP_ENV", "dev")
#     mock_mode: bool = os.getenv("MOCK_MODE", "true").lower() == "true"

#     # CORS
#     allowed_origins: list[str] = tuple(
#         o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
#     )

#     # Supabase
#     supabase_url: str = os.getenv("SUPABASE_URL", "")
#     supabase_key: str = os.getenv("SUPABASE_KEY", "")

#     # Bot
#     telegram_bot_username: str = os.getenv("TELEGRAM_BOT_USERNAME", "YourMILBot")

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
    
    # Bot Configuration
    telegram_bot_username: str = os.getenv("TELEGRAM_BOT_USERNAME", "YourMILBot")
    bot_token: str = os.getenv("BOT_TOKEN", "")
    
    # API Configuration
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000/api")  # Default to local dev
    
    # Webhook Configuration (Production)
    webhook_url: str = os.getenv("WEBHOOK_URL", "")
    webhook_secret_path: str = os.getenv("WEBHOOK_SECRET_PATH", "telegram-webhook-secret")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __post_init__(self):
        """Validate settings after initialization"""
        self.validate()
    
    def validate(self):
        """Validate required settings"""
        errors = []
        
        if not self.bot_token:
            errors.append("BOT_TOKEN is required")
        
        # Only require API_BASE_URL in production or when not in mock mode
        if not self.mock_mode and not self.api_base_url:
            errors.append("API_BASE_URL is required when not in mock mode")
        
        if self.app_env == "production":
            if not self.webhook_url:
                errors.append("WEBHOOK_URL is required in production")
            if not self.supabase_url:
                errors.append("SUPABASE_URL is required in production")
            if not self.supabase_key:
                errors.append("SUPABASE_KEY is required in production")
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.app_env in ("dev", "development", "local")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.app_env == "production"
    
    @property
    def use_polling(self) -> bool:
        """Determine if should use polling instead of webhooks"""
        return self.is_development or not self.webhook_url

# Create global settings instance
settings = Settings()
