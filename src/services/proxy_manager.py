"""Proxy management module"""
import json
import time
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

from curl_cffi.requests import AsyncSession

from ..core.database import Database
from ..core.models import ProxyConfig


class ProxyManager:
    """Proxy configuration manager"""

    PROXY_IP_CACHE_TTL = 600
    PROXY_IP_LOOKUP_TIMEOUT = 3
    PROXY_SCOPE_PRIORITY = {
        "generation": 0,
        "image_upload": 1,
        "request": 2,
        "pow": 3,
    }

    def __init__(self, db: Database):
        self.db = db
        self._proxy_ip_cache: Dict[str, Dict[str, Any]] = {}

    async def get_proxy_url(self, token_id: Optional[int] = None, proxy_url: Optional[str] = None) -> Optional[str]:
        """Get proxy URL for a token, with fallback to global proxy

        Args:
            token_id: Token ID (optional). If provided, returns token-specific proxy if set,
                     otherwise falls back to global proxy.
            proxy_url: Direct proxy URL (optional). If provided, returns this proxy URL directly.

        Returns:
            Proxy URL string or None
        """
        if proxy_url:
            return proxy_url

        if token_id is not None:
            token = await self.db.get_token(token_id)
            if token and token.proxy_url:
                return token.proxy_url

        config = await self.db.get_proxy_config()
        if config.proxy_enabled and config.proxy_url:
            return config.proxy_url
        return None

    async def get_image_upload_proxy_url(self, token_id: Optional[int] = None) -> Optional[str]:
        """Get proxy URL specifically for image uploads."""
        config = await self.db.get_proxy_config()
        if config.image_upload_proxy_enabled and config.image_upload_proxy_url:
            return config.image_upload_proxy_url

        return await self.get_proxy_url(token_id=token_id)

    def sanitize_proxy_url(self, proxy_url: Optional[str]) -> Optional[str]:
        """Mask proxy URL credentials and only keep scheme://host:port."""
        if not proxy_url:
            return None

        try:
            parsed = urlparse(proxy_url)
            scheme = parsed.scheme or "http"
            host = parsed.hostname
            port = parsed.port
            if host:
                if ":" in host and not host.startswith("["):
                    host = f"[{host}]"
                return f"{scheme}://{host}:{port}" if port else f"{scheme}://{host}"
        except Exception:
            pass

        if "://" in proxy_url:
            scheme, rest = proxy_url.split("://", 1)
        else:
            scheme, rest = "http", proxy_url
        rest = rest.rsplit("@", 1)[-1]
        return f"{scheme}://{rest}"

    async def lookup_proxy_egress(self, proxy_url: str) -> Dict[str, Optional[str]]:
        """Look up proxy egress IP and country info with in-memory TTL cache."""
        now = time.time()
        cached = self._proxy_ip_cache.get(proxy_url)
        if cached and cached["expires_at"] > now:
            return cached["data"]

        data = {
            "proxy_ip": None,
            "proxy_country": None,
            "proxy_country_code": None,
        }

        try:
            async with AsyncSession() as session:
                response = await session.get(
                    "https://ipwho.is/",
                    proxy=proxy_url,
                    timeout=self.PROXY_IP_LOOKUP_TIMEOUT,
                    impersonate="chrome",
                )
            if response.status_code == 200:
                payload = response.json()
                if payload.get("success", True):
                    data = {
                        "proxy_ip": payload.get("ip"),
                        "proxy_country": payload.get("country"),
                        "proxy_country_code": (payload.get("country_code") or "").upper() or None,
                    }
        except Exception:
            data = {
                "proxy_ip": None,
                "proxy_country": None,
                "proxy_country_code": None,
            }

        self._proxy_ip_cache[proxy_url] = {
            "expires_at": now + self.PROXY_IP_CACHE_TTL,
            "data": data,
        }
        return data

    async def resolve_proxy_snapshot(
        self,
        scope: str,
        token_id: Optional[int] = None,
        proxy_url: Optional[str] = None,
        use_image_upload_proxy: bool = False,
    ) -> Dict[str, Any]:
        """Resolve the current request proxy snapshot."""
        if proxy_url is None:
            if use_image_upload_proxy:
                proxy_url = await self.get_image_upload_proxy_url(token_id)
            else:
                proxy_url = await self.get_proxy_url(token_id=token_id)

        snapshot: Dict[str, Any] = {
            "scope": scope,
            "proxy_used": bool(proxy_url),
            "proxy_url_display": self.sanitize_proxy_url(proxy_url),
            "proxy_ip": None,
            "proxy_country": None,
            "proxy_country_code": None,
        }

        if proxy_url:
            snapshot.update(await self.lookup_proxy_egress(proxy_url))

        return snapshot

    def merge_proxy_trace(self, proxy_trace: Optional[List[Dict[str, Any]]], snapshot: Optional[Dict[str, Any]]) -> None:
        """Merge a proxy snapshot into a top-level request trace."""
        if proxy_trace is None or not snapshot:
            return

        normalized = {
            "scope": snapshot.get("scope"),
            "proxy_used": bool(snapshot.get("proxy_used")),
            "proxy_url_display": snapshot.get("proxy_url_display"),
            "proxy_ip": snapshot.get("proxy_ip"),
            "proxy_country": snapshot.get("proxy_country"),
            "proxy_country_code": snapshot.get("proxy_country_code"),
        }

        for index, item in enumerate(proxy_trace):
            if item.get("scope") == normalized["scope"]:
                proxy_trace[index] = normalized
                break
        else:
            proxy_trace.append(normalized)

        proxy_trace.sort(key=lambda item: self.PROXY_SCOPE_PRIORITY.get(item.get("scope"), 99))

    def build_log_proxy_payload(self, proxy_trace: Optional[List[Dict[str, Any]]]) -> Optional[Dict[str, Any]]:
        """Build request_logs fields from proxy trace snapshots."""
        if not proxy_trace:
            return None

        details = [
            {
                "scope": item.get("scope"),
                "proxy_used": bool(item.get("proxy_used")),
                "proxy_url_display": item.get("proxy_url_display"),
                "proxy_ip": item.get("proxy_ip"),
                "proxy_country": item.get("proxy_country"),
                "proxy_country_code": item.get("proxy_country_code"),
            }
            for item in sorted(
                proxy_trace,
                key=lambda value: self.PROXY_SCOPE_PRIORITY.get(value.get("scope"), 99),
            )
        ]

        primary = next((item for item in details if item["proxy_used"]), None)
        any_proxy_used = any(item["proxy_used"] for item in details)

        return {
            "proxy_used": any_proxy_used,
            "proxy_url_display": primary.get("proxy_url_display") if primary else None,
            "proxy_ip": primary.get("proxy_ip") if primary else None,
            "proxy_country": primary.get("proxy_country") if primary else None,
            "proxy_country_code": primary.get("proxy_country_code") if primary else None,
            "proxy_details": json.dumps(details, ensure_ascii=False),
        }

    async def update_proxy_config(
        self,
        enabled: bool,
        proxy_url: Optional[str],
        image_upload_proxy_enabled: bool = False,
        image_upload_proxy_url: Optional[str] = None
    ):
        """Update proxy configuration"""
        await self.db.update_proxy_config(
            enabled,
            proxy_url,
            image_upload_proxy_enabled,
            image_upload_proxy_url
        )

    async def get_proxy_config(self) -> ProxyConfig:
        """Get proxy configuration"""
        return await self.db.get_proxy_config()
