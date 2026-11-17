import httpx
from app.config import Settings


class CloudSync:
    """Server-side Supabase REST adapter. Service key must never reach the browser."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def insert(self, table: str, payload: dict) -> None:
        if not self.settings.cloud_configured:
            raise RuntimeError("Lovable Cloud ainda não configurado")
        base = self.settings.supabase_url.rstrip("/")
        url = f"{base}/rest/v1/{self.settings.supabase_table_prefix}{table}"
        headers = {
            "apikey": self.settings.supabase_service_role_key,
            "Authorization": f"Bearer {self.settings.supabase_service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
