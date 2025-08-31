
from vistock.core.constants import (
    DEFAULT_VIETSTOCK_STOCK_INDEX_BASE_URL,
    DEFAULT_VIETSTOCK_DOMAIN,
    DEFAULT_TIMEOUT
)
from vistock.core.models import (
    StandardStockIndexSearchResults,
    AdvancedStockIndexSearchResults
)
from vistock.core.enums import (
    VistockPeriodCode,
    VistockResolutionCode
)
from vistock.core.interfaces.ivistocksearch import (
    IVistockStockIndexSearch,
    AsyncIVistockStockIndexSearch
)
from vistock.modules.vietstock.fetchers import (
    VistockVietstockAPIFetcher
)
from vistock.modules.vietstock.parsers import (
    VistockVietstockStockIndexParser
)
from vistock.core.utils import (
    VistockConverter,
    VistockGenerator
)
from typing import List, Dict, Union, Any, Optional
from datetime import datetime
import asyncio

class VistockVietstockStockIndexSearch(IVistockStockIndexSearch, AsyncIVistockStockIndexSearch):
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
        self._base_url = DEFAULT_VIETSTOCK_STOCK_INDEX_BASE_URL
        self._domain = DEFAULT_VIETSTOCK_DOMAIN
        self._fetcher = VistockVietstockAPIFetcher()
        self._parser = VistockVietstockStockIndexParser()

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
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL,
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY,
        advanced: bool = False,
        ascending: bool = True
    ) -> Union[StandardStockIndexSearchResults, AdvancedStockIndexSearchResults]:
        if not start_date:
            start_date = VistockGenerator.generate_start_date(period=period)

        url = f'{self._base_url}{self._parser.to_query(code=code, start_date=start_date, end_date=end_date)}'

        response = self._fetcher.fetch(url=url)

        data: List[Dict[str, Any]] = []
        if response.get('s') == 'ok':
            mopens = response.get('o', [])
            mhighs = response.get('h', [])
            mlows = response.get('l', [])
            mcloses = response.get('c', [])
            nmvolumes = response.get('v', [])
            timestamps = response.get('t', [])

            for mopen, mhigh, mlow, mclose, nmvolume, timestamp in zip(mopens, mhighs, mlows, mcloses, nmvolumes, timestamps):
                data.append({
                    'code': code,
                    'date': VistockConverter.from_timestamp_to_date(timestamp=timestamp),
                    'floor': '',
                    'adOpen': mopen,
                    'adHigh': mhigh,
                    'adLow': mlow,
                    'adClose': mclose,
                    'nmVolume': nmvolume
                })

        if not data:
            if isinstance(period, str) and period != '1D':
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                )
            
            if isinstance(period, VistockPeriodCode) and period != VistockPeriodCode.ONE_DAY:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                )
            
            url = f'{self._base_url}{self._parser.to_query(code=code, end_date=end_date)}'

            response = self._fetcher.fetch(url=url)

            data: List[Dict[str, Any]] = []
            if response.get('s') == 'ok':
                mopens = response.get('o', [])
                mhighs = response.get('h', [])
                mlows = response.get('l', [])
                mcloses = response.get('c', [])
                nmvolumes = response.get('v', [])
                timestamps = response.get('t', [])

                for mopen, mhigh, mlow, mclose, nmvolume, timestamp in zip(mopens, mhighs, mlows, mcloses, nmvolumes, timestamps):
                    data.append({
                        'code': code,
                        'date': VistockConverter.from_timestamp_to_date(timestamp=timestamp),
                        'floor': '',
                        'adOpen': mopen,
                        'adHigh': mhigh,
                        'adLow': mlow,
                        'adClose': mclose,
                        'nmVolume': nmvolume
                    })
            data = [data[0 if ascending else -1]]
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{data[0].get('date', 0)}", end_date="{end_date}". Please verify the input parameters and try again.'
                )
            
        data = self._parser.to_resolution(data=data, resolution=resolution)
        data.sort(key=lambda x: x.get('date', ''), reverse=not ascending)

        if advanced and resolution == VistockResolutionCode.DAY:
            return self._parser.to_advanced(data=data)

        return self._parser.to_standard(data=data)

    async def async_search(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL,
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY,
        advanced: bool = False,
        ascending: bool = True    
    ) -> Union[StandardStockIndexSearchResults, AdvancedStockIndexSearchResults]:
        if not start_date:
            start_date = VistockGenerator.generate_start_date(period=period)

        url = f'{self._base_url}{self._parser.to_query(code=code, start_date=start_date, end_date=end_date)}'

        response = await self._fetcher.async_fetch(url=url)

        data: List[Dict[str, Any]] = []
        if response.get('s') == 'ok':
            mopens = response.get('o', [])
            mhighs = response.get('h', [])
            mlows = response.get('l', [])
            mcloses = response.get('c', [])
            nmvolumes = response.get('v', [])
            timestamps = response.get('t', [])

            for mopen, mhigh, mlow, mclose, nmvolume, timestamp in zip(mopens, mhighs, mlows, mcloses, nmvolumes, timestamps):
                data.append({
                    'code': code,
                    'date': VistockConverter.from_timestamp_to_date(timestamp=timestamp),
                    'floor': '',
                    'adOpen': mopen,
                    'adHigh': mhigh,
                    'adLow': mlow,
                    'adClose': mclose,
                    'nmVolume': nmvolume
                })

        if not data:
            if isinstance(period, str) and period != '1D':
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                )
            
            if isinstance(period, VistockPeriodCode) and period != VistockPeriodCode.ONE_DAY:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                )
            
            url = f'{self._base_url}{self._parser.to_query(code=code, end_date=end_date)}'

            response = await self._fetcher.async_fetch(url=url)

            data: List[Dict[str, Any]] = []
            if response.get('s') == 'ok':
                mopens = response.get('o', [])
                mhighs = response.get('h', [])
                mlows = response.get('l', [])
                mcloses = response.get('c', [])
                nmvolumes = response.get('v', [])
                timestamps = response.get('t', [])

                for mopen, mhigh, mlow, mclose, nmvolume, timestamp in zip(mopens, mhighs, mlows, mcloses, nmvolumes, timestamps):
                    data.append({
                        'code': code,
                        'date': VistockConverter.from_timestamp_to_date(timestamp=timestamp),
                        'floor': '',
                        'adOpen': mopen,
                        'adHigh': mhigh,
                        'adLow': mlow,
                        'adClose': mclose,
                        'nmVolume': nmvolume
                    })
            data = [data[0 if ascending else -1]]
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{data[0].get('date', 0)}", end_date="{end_date}". Please verify the input parameters and try again.'
                )
            
        data = self._parser.to_resolution(data=data, resolution=resolution)
        data.sort(key=lambda x: x.get('date', ''), reverse=not ascending)

        if advanced and resolution == VistockResolutionCode.DAY:
            return self._parser.to_advanced(data=data)

        return self._parser.to_standard(data=data)