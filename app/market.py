import httpx
from app.models import PriceSnapshot


class MarketDataError(RuntimeError):
    pass


class CoinGeckoPriceProvider:
    """Fetches the BTC/BRL spot quote from CoinGecko's public API."""

    URL = "https://api.coingecko.com/api/v3/simple/price"

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key

    async def get_btc_brl(self) -> PriceSnapshot:
        headers = {"x-cg-demo-api-key": self.api_key} if self.api_key else {}
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.get(
                    self.URL,
                    params={"ids": "bitcoin", "vs_currencies": "brl"},
                    headers=headers,
                )
                response.raise_for_status()
                value = float(response.json()["bitcoin"]["brl"])
                return PriceSnapshot(symbol="BTCBRL", price_brl=value, source="coingecko")
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise MarketDataError(f"Não foi possível obter cotação BTC/BRL: {exc}") from exc
