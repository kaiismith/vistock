from typing import Dict, Any

class IVistockAPIFetcher:
    def fetch(self, url: str) -> Dict[str, Any]:
        ...

class AsyncIVistockAPIFetcher:
    async def async_fetch(self, url: str) -> Dict[str, Any]:
        ...

class IVistockAPIWithPayloadFetcher:
    def fetch(
        self,
        url: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        ...

class AsyncIVistockAPIWithPayloadFetcher:
    async def async_fetch(
        self,
        url: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        ...