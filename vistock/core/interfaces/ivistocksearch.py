from vistock.core.models import (
    StandardStockIndexSearchResults,
    AdvancedStockIndexSearchResults,
    StandardFundamentalIndexSearchResults,
    StandardFinancialModelsSearchResults,
    StandardFinancialStatementsIndexSearchResults,
    StandardMarketPricesSearchResults,
    AdvancedMarketPricesSearchResults,
    StandardChangePricesSearchResults,
    StandardStockListingSearchResults,
    StandardTradingIndexSearchResults
)
from vistock.core.enums import (
    VistockIndustryCategory,
    VistockFloorCategory,
    VistockCompanyTypeCategory,
    VistockLetterCategory,
    VistockFinancialModelsCategory,
    VistockReportTypeCategory,
    VistockIndexCode,
    VistockPeriodCode,
    VistockResolutionCode
)
from typing import Union, Optional, Protocol
from datetime import datetime, timezone

class IVistockStockIndexSearch(Protocol):
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
        ...

class AsyncIVistockStockIndexSearch(Protocol):
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
        ...

class IVistockFundamentalIndexSearch(Protocol):
    def search(
        self,
        code: str
    ) -> StandardFundamentalIndexSearchResults:
        ...

class AsyncIVistockFundamentalIndexSearch(Protocol):
    async def async_search(
        self,
        code: str
    ) -> StandardFundamentalIndexSearchResults:
        ...

class IVistockFinancialModelsSearch(Protocol):
    def search(
        self,
        code: str,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialModelsSearchResults:
        ...

class AsyncIVistockFinancialModelsSearch(Protocol):
    async def async_search(
        self,
        code: str,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialModelsSearchResults:
        ...

class IVistockFinancialStatementsIndexSearch(Protocol):
    def search(
        self,
        code: str,
        start_year: Optional[int] = None,
        end_year: int = datetime.now().year,
        report: Union[VistockReportTypeCategory, str] = VistockReportTypeCategory.ANNUAL,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialStatementsIndexSearchResults:
        ...

class AsyncIVistockFinancialStatementsIndexSearch(Protocol):
    async def async_search(
        self,
        code: str,
        start_year: Optional[int] = None,
        end_year: int = datetime.now().year,
        report: Union[VistockReportTypeCategory, str] = VistockReportTypeCategory.ANNUAL,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> StandardFinancialStatementsIndexSearchResults:
        ...

class IVistockMarketPricesSearch(Protocol):
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
        ...

class AsyncIVistockMarketPricesSearch(Protocol):
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
        ...

class IVistockChangePricesSearch(Protocol):
    def search(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL
    ) -> StandardChangePricesSearchResults:
        ...

class AsyncIVistockChangePricesSearch(Protocol):
    async def async_search(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL
    ) -> StandardChangePricesSearchResults:
        ...

class IVistockStockListingSearch(Protocol):
    def search(
        self,
        industry: Union[VistockIndustryCategory, str] = VistockIndustryCategory.ALL,
        floor: Union[VistockFloorCategory, str] = VistockFloorCategory.ALL,
        company_type: Union[VistockCompanyTypeCategory, str] = VistockCompanyTypeCategory.ALL,
        letter: Union[VistockLetterCategory, str] = VistockLetterCategory.ALL
    ) -> StandardStockListingSearchResults:
        ...

class AsyncIVistockStockListingSearch(Protocol):
    async def async_search(
        self,
        industry: Union[VistockIndustryCategory, str] = VistockIndustryCategory.ALL,
        floor: Union[VistockFloorCategory, str] = VistockFloorCategory.ALL,
        company_type: Union[VistockCompanyTypeCategory, str] = VistockCompanyTypeCategory.ALL,
        letter: Union[VistockLetterCategory, str] = VistockLetterCategory.ALL
    ) -> StandardStockListingSearchResults:
        ...

class IVistockTradingIndexSearch(Protocol):
    def search(
        self,
        code: str,
        current_datetime: str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        ascending: bool = False
    ) -> StandardTradingIndexSearchResults:
        ...

class AsyncIVistockTradingIndexSearch(Protocol):
    async def async_search(
        self,
        code: str,
        current_datetime: str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        ascending: bool = False
    ) -> StandardTradingIndexSearchResults:
        ...