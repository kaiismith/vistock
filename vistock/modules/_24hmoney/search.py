from vistock.core.constants import (
    DEFAULT_24HMONEY_BASE_URL,
    DEFAULT_24HMONEY_DOMAIN,
    DEFAULT_TIMEOUT
)
from vistock.core.models import (
    StandardStockListingSearchResults
)
from vistock.core.enums import (
    VistockIndustryCategory,
    VistockFloorCategory,
    VistockCompanyTypeCategory,
    VistockLetterCategory
)
from vistock.core.interfaces.ivistocksearch import (
    IVistockStockListingSearch,
    AsyncIVistockStockListingSearch
)
from vistock.modules._24hmoney.fetchers import (
    Vistock24HMoneyAPIFetcher
)
from vistock.modules._24hmoney.parsers import (
    Vistock24HMoneyStockListingParser
)
from typing import List, Dict, Union, Any
import asyncio

class Vistock24HMoneyStockListingSearch(IVistockStockListingSearch, AsyncIVistockStockListingSearch):
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
        self._base_url = DEFAULT_24HMONEY_BASE_URL
        self._domain = DEFAULT_24HMONEY_DOMAIN
        self._fetcher = Vistock24HMoneyAPIFetcher()
        self._parser = Vistock24HMoneyStockListingParser()

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
        industry: Union[VistockIndustryCategory, str] = VistockIndustryCategory.ALL,
        floor: Union[VistockFloorCategory, str] = VistockFloorCategory.ALL,
        company_type: Union[VistockCompanyTypeCategory, str] = VistockCompanyTypeCategory.ALL,
        letter: Union[VistockLetterCategory, str] = VistockLetterCategory.ALL
    ) -> StandardStockListingSearchResults:
        url = f'{self._base_url}{self._parser.to_query(industry=industry, floor=floor, company_type=company_type, letter=letter)}'

        response = self._fetcher.fetch(url=url)

        data: List[Dict[str, Any]] = response.get('data', []).get('data', [])
        if not data:
            raise ValueError(
                f'No data found for the given parameters: industry="{industry}", floor="{floor}", company_type="{company_type}", letter="{letter}". Please verify the input parameters and try again.'
            )
        
        return self._parser.to_standard(data=data)

    async def async_search(
        self,
        industry: Union[VistockIndustryCategory, str] = VistockIndustryCategory.ALL,
        floor: Union[VistockFloorCategory, str] = VistockFloorCategory.ALL,
        company_type: Union[VistockCompanyTypeCategory, str] = VistockCompanyTypeCategory.ALL,
        letter: Union[VistockLetterCategory, str] = VistockLetterCategory.ALL
    ) -> StandardStockListingSearchResults:
        url = f'{self._base_url}{self._parser.to_query(industry=industry, floor=floor, company_type=company_type, letter=letter)}'

        response = await self._fetcher.async_fetch(url=url)

        data: List[Dict[str, Any]] = response.get('data', []).get('data', [])
        if not data:
            raise ValueError(
                f'No data found for the given parameters: industry="{industry}", floor="{floor}", company_type="{company_type}", letter="{letter}". Please verify the input parameters and try again.'
            )
        
        return self._parser.to_standard(data=data)