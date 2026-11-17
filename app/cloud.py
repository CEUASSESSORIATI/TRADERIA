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
        params = {"on_conflict": "id"} if table == "paper_trades" else None
        headers = {
            "apikey": self.settings.supabase_service_role_key,
            "Authorization": f"Bearer {self.settings.supabase_service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
