from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8787
    api_access_token: str = Field(default="CHANGE_ME_TO_A_LONG_RANDOM_SECRET")
    trading_mode: str = "paper"
    trading_symbol: str = "BTCBRL"
    initial_capital_brl: float = 100.0
    trading_cycle_seconds: int = 30
    max_daily_loss_pct: float = 3.0
    max_drawdown_pct: float = 8.0
    max_position_pct: float = 25.0
    paper_fee_pct: float = 0.1
    paper_slippage_pct: float = 0.05
    price_provider: str = "coingecko"
    coingecko_demo_api_key: str = ""
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_table_prefix: str = "cti_"
    outbox_db_path: str = "./data/outbox.sqlite3"
    log_level: str = "INFO"

    @property
    def outbox_path(self) -> Path:
        path = Path(self.outbox_db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def cloud_configured(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
