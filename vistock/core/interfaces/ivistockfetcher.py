from typing import Dict, Any, Protocol

class IVistockAPIFetcher(Protocol):
    def fetch(self, url: str) -> Dict[str, Any]:
        ...

class AsyncIVistockAPIFetcher(Protocol):
    async def async_fetch(self, url: str) -> Dict[str, Any]:
        ...

class IVistockAPIWithPayloadFetcher(Protocol):
    def fetch(
        self,
        url: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        ...

class AsyncIVistockAPIWithPayloadFetcher(Protocol):
    async def async_fetch(
        self,
        url: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        ...