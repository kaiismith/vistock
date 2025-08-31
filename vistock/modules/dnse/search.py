
from vistock.core.constants import (
    DEFAULT_DNSE_TRADING_INDEX_BASE_URL,
    DEFAULT_DNSE_DOMAIN,
    DEFAULT_TIMEOUT
)
from vistock.core.models import (
    StandardTradingIndexSearchResults
)
from vistock.core.interfaces.ivistocksearch import (
    IVistockTradingIndexSearch,
    AsyncIVistockTradingIndexSearch
)
from vistock.modules.dnse.fetchers import (
    VistockDNSEAPIFetcher
)
from vistock.modules.dnse.parsers import (
    VistockDNSETradingIndexParser
)
from datetime import datetime, timezone
from typing import List, Dict, Any
import asyncio

class VistockDNSETradingIndexSearch(IVistockTradingIndexSearch, AsyncIVistockTradingIndexSearch):
    def __init__(self, timeout: float = DEFAULT_TIMEOUT, **kwargs: Any) -> None:
        if timeout <= 0:
            raise ValueError(
                'Invalid configuration: "timeout" must be a strictly positive integer value representing the maximum allowable wait time for the operation.'
            )
        
        if 'semaphore_limit' in kwargs and (not isinstance(kwargs['semaphore_limit'], int) or kwargs['semaphore_limit'] <= 0):
            raise ValueError(
                'Invalid configuration: "semaphore_limit" must be a positive integer, indicating the maximum number of concurrent asynchronous operations permitted.'
            )
        
        self._timeout = timeout
        self._semaphore_limit = kwargs.get('semaphore_limit', 5)
        self._semaphore = asyncio.Semaphore(self._semaphore_limit)
        self._base_url = DEFAULT_DNSE_TRADING_INDEX_BASE_URL
        self._domain = DEFAULT_DNSE_DOMAIN
        self._fetcher = VistockDNSEAPIFetcher()
        self._parser = VistockDNSETradingIndexParser()

    @property
    def timeout(self) -> float:
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: int) -> None:
        if value <= 0:
            raise ValueError(
                'Invalid configuration: "timeout" must be a strictly positive integer value representing the maximum allowable wait time for the operation.'
            )
        self._timeout = value

    def search(
        self,
        code: str,
        current_datetime: str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        ascending: bool = False
    ) -> StandardTradingIndexSearchResults:
        payload = self._parser.to_payload(
            code=code,
            current_datetime=current_datetime
        )

        response = self._fetcher.fetch(
            url=self._base_url,
            payload=payload
        )

        data: List[Dict[str, Any]] = response.get('data', {}).get('GetKrxTicksBySymbols', {}).get('ticks', [])
        if not data:
            raise ValueError(
                f'No data found for the given parameters: code="{code}". Please verify the input parameters and try again.'
            )
        
        data.sort(key=lambda x: x.get('sendingTime', ''), reverse=not ascending)

        return self._parser.to_standard(data=data)

    async def async_search(
        self,
        code: str,
        current_datetime: str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        ascending: bool = False
    ) -> StandardTradingIndexSearchResults:
        payload = self._parser.to_payload(
            code=code,
            current_datetime=current_datetime
        )

        response = await self._fetcher.async_fetch(
            url=self._base_url,
            payload=payload
        )

        data: List[Dict[str, Any]] = response.get('data', {}).get('GetKrxTicksBySymbols', {}).get('ticks', [])
        if not data:
            raise ValueError(
                f'No data found for the given parameters: code="{code}". Please verify the input parameters and try again.'
            )
        
        data.sort(key=lambda x: x.get('sendingTime', ''), reverse=not ascending)

        return self._parser.to_standard(data=data)