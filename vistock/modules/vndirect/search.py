from vistock.core.constants import (
    DEFAULT_VNDIRECT_STOCK_INDEX_BASE_URL,
    DEFAULT_VNDIRECT_FUNDAMENTAL_INDEX_BASE_URL,
    DEFAULT_VNDIRECT_FINANCIAL_MODELS_BASE_URL,
    DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_BASE_URL,
    DEFAULT_VNDIRECT_MARKET_PRICES_URL,
    DEFAULT_VNDIRECT_CHANGE_PRICES_URL,
    DEFAULT_VNDIRECT_DOMAIN, 
    DEFAULT_TIMEOUT
)
from vistock.core.models import (
    StandardStockIndexSearchResults,
    AdvancedStockIndexSearchResults,
    StandardFundamentalIndexSearchResults,
    StandardFinancialModelsSearchResults,
    StandardFinancialStatementsIndexSearchResults,
    StandardMarketPricesSearchResults,
    AdvancedMarketPricesSearchResults,
    StandardChangePricesSearchResults
)
from vistock.core.enums import (
    VistockPeriodCode,
    VistockResolutionCode,
    VistockFinancialModelsCategory,
    VistockReportTypeCategory,
    VistockIndexCode
)
from vistock.core.interfaces.ivistocksearch import (
    IVistockStockIndexSearch,
    AsyncIVistockStockIndexSearch,
    IVistockFundamentalIndexSearch,
    AsyncIVistockFundamentalIndexSearch,
    IVistockFinancialModelsSearch,
    AsyncIVistockFinancialModelsSearch,
    IVistockFinancialStatementsIndexSearch,
    AsyncIVistockFinancialStatementsIndexSearch,
    IVistockMarketPricesSearch,
    AsyncIVistockMarketPricesSearch,
    IVistockChangePricesSearch,
    AsyncIVistockChangePricesSearch
)
from vistock.modules.vndirect.fetchers import (
    VistockVndirectAPIFetcher
)
from vistock.modules.vndirect.parsers import (
    VistockVndirectStockIndexParser,
    VistockVndirectFundamentalIndexParser,
    VistockVndirectFinancialModelsParser,
    VistockVndirectFinancialStatementsIndexParser,
    VistockVndirectMarketPricesParser,
    VistockVndirectChangePricesParser
)
from vistock.core.utils import (
    VistockGenerator, 
)
from typing import List, Dict, Union, Optional, Any
from datetime import datetime
import asyncio

class VistockVndirectStockIndexSearch(IVistockStockIndexSearch, AsyncIVistockStockIndexSearch):
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
        self._base_url = DEFAULT_VNDIRECT_STOCK_INDEX_BASE_URL
        self._domain = DEFAULT_VNDIRECT_DOMAIN
        self._fetcher = VistockVndirectAPIFetcher()
        self._parser = VistockVndirectStockIndexParser()

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
        advanced: bool = True,
        ascending: bool = True
    ) -> Union[StandardStockIndexSearchResults, AdvancedStockIndexSearchResults]:
        if not start_date:
            start_date = VistockGenerator.generate_start_date(period=period)

        url = f'{self._base_url}{self._parser.to_query(code=code, start_date=start_date, end_date=end_date)}'

        response = self._fetcher.fetch(url=url)

        data: List[Dict[str, Any]] = response.get('data', [])
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

            data: List[Dict[str, Any]] = [response.get('data', [])[0 if ascending else -1]] if response.get('data') else []
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
        advanced: bool = True,
        ascending: bool = True
    ) -> Union[StandardStockIndexSearchResults, AdvancedStockIndexSearchResults]:
        if not start_date:
            start_date = VistockGenerator.generate_start_date(period=period)

        url = f'{self._base_url}{self._parser.to_query(code=code, start_date=start_date, end_date=end_date)}'

        response = await self._fetcher.async_fetch(url=url)
        
        data: List[Dict[str, Any]] = response.get('data', [])
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

            data: List[Dict[str, Any]] = [response.get('data', [])[-1 if ascending else 0]] if response.get('data') else []
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_date="{data[0].get('date', 0)}", end_date="{end_date}". Please verify the input parameters and try again.'
                )

        data = self._parser.to_resolution(data=data, resolution=resolution)
        data.sort(key=lambda x: x.get('date', ''), reverse=not ascending)

        if advanced and resolution == VistockResolutionCode.DAY:
            return self._parser.to_advanced(data=data)
        
        return self._parser.to_standard(data=data)
    
class VistockVndirectFundamentalIndexSearch(IVistockFundamentalIndexSearch, AsyncIVistockFundamentalIndexSearch):
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
        self._base_url = DEFAULT_VNDIRECT_FUNDAMENTAL_INDEX_BASE_URL
        self._domain = DEFAULT_VNDIRECT_DOMAIN
        self._fetcher = VistockVndirectAPIFetcher()
        self._parser = VistockVndirectFundamentalIndexParser()

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

    def search(self, code: str) -> StandardFundamentalIndexSearchResults:
        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(code=code)
        for query in queries:
            url = f'{self._base_url}{query}'
            response = self._fetcher.fetch(url=url)
            data: List[Dict[str, Any]] = response.get('data', [])

            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}". Please verify the input parameters and try again.'
                )
            
            results.append(data)

        merged_results = [item for result in results for item in result]

        ratio = {item.get('ratioCode', '').upper(): item.get('value', 0.0) for item in merged_results}

        return self._parser.to_standard(code=code, ratio=ratio)
    
    async def async_search(self, code: str) -> StandardFundamentalIndexSearchResults:
        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(code=code)
        for query in queries:
            url = f'{self._base_url}{query}'
            response = await self._fetcher.async_fetch(url=url)
            data: List[Dict[str, Any]] = response.get('data', [])

            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}". Please verify the input parameters and try again.'
                )
            
            results.append(data)

        merged_results = [item for result in results for item in result]

        ratio = {item.get('ratioCode', '').upper(): item.get('value', 0.0) for item in merged_results}

        return self._parser.to_standard(code=code, ratio=ratio)
    
class VistockVndirectFinancialModelsSearch(IVistockFinancialModelsSearch, AsyncIVistockFinancialModelsSearch):
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
        self._base_url = DEFAULT_VNDIRECT_FINANCIAL_MODELS_BASE_URL
        self._domain = DEFAULT_VNDIRECT_DOMAIN
        self._fetcher = VistockVndirectAPIFetcher()
        self._parser = VistockVndirectFinancialModelsParser()

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
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialModelsSearchResults:
        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(code=code, model=model)
        for query in queries:
            url = f'{self._base_url}{query}'

            response = self._fetcher.fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", model="{model}". Please verify the input parameters and try again.'
                )
            results.append(data)

        models = [item for result in results for item in result]

        return self._parser.to_standard(code=code, models=models)
    
    async def async_search(
        self,
        code: str,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialModelsSearchResults:
        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(code=code, model=model)
        for query in queries:
            url = f'{self._base_url}{query}'

            response = await self._fetcher.async_fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", model="{model}". Please verify the input parameters and try again.'
                )
            results.append(data)

        models = [item for result in results for item in result]

        return self._parser.to_standard(code=code, models=models)
    
class VistockVndirectFinancialStatementsIndexSearch(IVistockFinancialStatementsIndexSearch, AsyncIVistockFinancialStatementsIndexSearch):
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
        self._base_url = DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_BASE_URL
        self._domain = DEFAULT_VNDIRECT_DOMAIN
        self._fetcher = VistockVndirectAPIFetcher()
        self._parser = VistockVndirectFinancialStatementsIndexParser()
        self._models_search = VistockVndirectFinancialModelsSearch()

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
        start_year: Optional[int] = None,
        end_year: int = datetime.now().year,
        report: Union[VistockReportTypeCategory, str] = VistockReportTypeCategory.ANNUAL,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialStatementsIndexSearchResults:
        statements: List[Dict[str, Any]] = []

        queries = self._parser.to_query(
            code=code,
            start_year=start_year,
            end_year=end_year,
            report=report,
            model=model
        )

        for query in queries:
            url = f'{self._base_url}{query}'
            
            response = self._fetcher.fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_year="{start_year}, end_year="{end_year}", report="{report}", "model="{model}". Please verify the input parameters and try again.'
                )
            
            statements.extend(data)

        return self._parser.to_standard(
            models=self._models_search.search(code=code, model=model),
            statements=statements
        )

    async def async_search(
        self,
        code: str,
        start_year: Optional[int] = None,
        end_year: int = datetime.now().year,
        report: Union[VistockReportTypeCategory, str] = VistockReportTypeCategory.ANNUAL,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialStatementsIndexSearchResults:
        statements: List[Dict[str, Any]] = []

        queries = self._parser.to_query(
            code=code,
            start_year=start_year,
            end_year=end_year,
            report=report,
            model=model
        )

        for query in queries:
            url = f'{self._base_url}{query}'
            
            response = await self._fetcher.async_fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", start_year="{start_year}, end_year="{end_year}", report="{report}", "model="{model}". Please verify the input parameters and try again.'
                )
            
            statements.extend(data)

        return self._parser.to_standard(
            models=await self._models_search.async_search(code=code, model=model),
            statements=statements
        )
    
class VistockVndirectMarketPricesSearch(IVistockMarketPricesSearch, AsyncIVistockMarketPricesSearch):
    def __init__(self, timeout: float = DEFAULT_TIMEOUT, **kwargs: Any) -> None:
        if timeout <= 0:
            raise ValueError(
                'Invalid configuration: "timeout" must be a strictly positive integer value representing the maximum allowable wait time for the operation.'
            )
        self._timeout = timeout

        if 'semaphore_limit' in kwargs and (not isinstance(kwargs['semaphore_limit'], int) or kwargs['semaphore_limit'] <= 0):
            raise ValueError(
                'Invalid configuration: "semaphore_limit" must be a positive integer, indicating the maximum number of concurrent asynchronous operations permitted.'
            )

        self._timeout = timeout
        self._semaphore_limit = kwargs.get('semaphore_limit', 5)
        self._semaphore = asyncio.Semaphore(self._semaphore_limit)
        self._base_url = DEFAULT_VNDIRECT_MARKET_PRICES_URL
        self._domain = DEFAULT_VNDIRECT_DOMAIN
        self._fetcher = VistockVndirectAPIFetcher()
        self._parser = VistockVndirectMarketPricesParser()

    @property
    def timeout(self) -> float:
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: int) -> None:
        if value <= 0:
            raise ValueError(
                'Invalid value: "timeout" must be a positive integer greater than zero.'
            )
        self._timeout = value

    def search(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL,
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY,
        advanced: bool = True,
        ascending: bool = True
    ) -> Union[StandardMarketPricesSearchResults, AdvancedMarketPricesSearchResults]:
        if not start_date:
            start_date = VistockGenerator.generate_start_date(period=period)

        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(
            code=code, 
            start_date=start_date, 
            end_date=end_date, 
            ascending=ascending
        )
        for query in queries:
            url = f'{self._base_url}{query}'

            response = self._fetcher.fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                if isinstance(period, str) and period != '1D':
                    raise ValueError(
                        f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                    )
                
                if isinstance(period, VistockPeriodCode) and period != VistockPeriodCode.ONE_DAY:
                    raise ValueError(
                        f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                    )
                
                queries = self._parser.to_query(
                    code=code,
                    ascending=ascending
                )

                for query in queries:
                    url = f'{self._base_url}{query}'

                    response = self._fetcher.fetch(url=url)

                    data: List[Dict[str, Any]] = [response.get('data', [])[-1 if ascending else 0]] if response.get('data') else []
                    if not data:
                        raise ValueError(
                            f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                        )

            results.append(data)

        prices = [item for result in results for item in result]

        if advanced:
            return self._parser.to_advanced(prices=prices)

        return self._parser.to_standard(prices=prices)
    
    async def async_search(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL,
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY,
        advanced: bool = True,
        ascending: bool = True
    ) -> Union[StandardMarketPricesSearchResults, AdvancedMarketPricesSearchResults]:
        if not start_date:
            start_date = VistockGenerator.generate_start_date(period=period)

        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(
            code=code, 
            start_date=start_date, 
            end_date=end_date, 
            ascending=ascending
        )
        for query in queries:
            url = f'{self._base_url}{query}'

            response = await self._fetcher.async_fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                if isinstance(period, str) and period != '1D':
                    raise ValueError(
                        f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                    )
                
                if isinstance(period, VistockPeriodCode) and period != VistockPeriodCode.ONE_DAY:
                    raise ValueError(
                        f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                    )
                
                queries = self._parser.to_query(
                    code=code,
                    ascending=ascending
                )

                for query in queries:
                    url = f'{self._base_url}{query}'

                    response = await self._fetcher.async_fetch(url=url)

                    data: List[Dict[str, Any]] = [response.get('data', [])[-1 if ascending else 0]] if response.get('data') else []
                    if not data:
                        raise ValueError(
                            f'No data found for the given parameters: code="{code}", start_date="{start_date}", end_date="{end_date}". Please verify the input parameters and try again.'
                        )
                    
                    data = self._parser.to_resolution(data=data, resolution=resolution)

            data = self._parser.to_resolution(data=data, resolution=resolution)

            results.append(data)

        prices = [item for result in results for item in result]

        if advanced and resolution == VistockResolutionCode.DAY:
            return self._parser.to_advanced(prices=prices)

        return self._parser.to_standard(prices=prices)
    
class VistockVndirectChangePricesSearch(IVistockChangePricesSearch, AsyncIVistockChangePricesSearch):
    def __init__(self, timeout: float = DEFAULT_TIMEOUT, **kwargs: Any) -> None:
        if timeout <= 0:
            raise ValueError(
                'Invalid configuration: "timeout" must be a strictly positive integer value representing the maximum allowable wait time for the operation.'
            )
        self._timeout = timeout

        if 'semaphore_limit' in kwargs and (not isinstance(kwargs['semaphore_limit'], int) or kwargs['semaphore_limit'] <= 0):
            raise ValueError(
                'Invalid configuration: "semaphore_limit" must be a positive integer, indicating the maximum number of concurrent asynchronous operations permitted.'
            )

        self._timeout = timeout
        self._semaphore_limit = kwargs.get('semaphore_limit', 5)
        self._semaphore = asyncio.Semaphore(self._semaphore_limit)
        self._base_url = DEFAULT_VNDIRECT_CHANGE_PRICES_URL
        self._domain = DEFAULT_VNDIRECT_DOMAIN
        self._fetcher = VistockVndirectAPIFetcher()
        self._parser = VistockVndirectChangePricesParser()

    @property
    def timeout(self) -> float:
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: int) -> None:
        if value <= 0:
            raise ValueError(
                'Invalid value: "timeout" must be a positive integer greater than zero.'
            )
        self._timeout = value

    def search(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL
    ) -> StandardChangePricesSearchResults:
        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(
            code=code,
            period=period
        )
        for query in queries:
            url = f'{self._base_url}{query}'
        
            response = self._fetcher.fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", period="{period}"". Please verify the input parameters and try again.'
                )
            
            results.append(data)

        prices = [item for result in results for item in result]
        
        return self._parser.to_standard(prices=prices)
    
    async def async_search(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL
    ) -> StandardChangePricesSearchResults:
        results: List[List[Dict[str, Any]]] = []

        queries = self._parser.to_query(
            code=code,
            period=period
        )
        for query in queries:
            url = f'{self._base_url}{query}'
        
            response = await self._fetcher.async_fetch(url=url)

            data: List[Dict[str, Any]] = response.get('data', [])
            if not data:
                raise ValueError(
                    f'No data found for the given parameters: code="{code}", period="{period}"". Please verify the input parameters and try again.'
                )
            
            results.append(data)

        prices = [item for result in results for item in result]
        
        return self._parser.to_standard(prices=prices)
