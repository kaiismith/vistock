from vistock.core.enums import (
    VistockIndexCode,
    VistockPeriodCode,
    VistockResolutionCode,
    VistockIndustryCategory,
    VistockFloorCategory,
    VistockCompanyTypeCategory,
    VistockLetterCategory,
    VistockFinancialModelsCategory,
    VistockReportTypeCategory
)
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
from typing import List, Dict, Union, Any, Optional, Protocol
from datetime import datetime, timezone

class IVistockStockIndexParser(Protocol):
    def to_query(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d')
    ) -> str:
        ...

    def to_resolution(
        self, 
        data: List[Dict[str, Any]], 
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY
    ) -> List[Dict[str, Any]]:
        ...

    def to_standard(
        self, 
        data: List[Dict[str, Any]]
    ) -> StandardStockIndexSearchResults:
        ...

    def to_advanced(
        self, 
        data: List[Dict[str, Any]]
    ) -> AdvancedStockIndexSearchResults:
        ...

class IVistockFundamentalIndexParser(Protocol):
    def to_query(
        self,
        code: str
    ) -> List[str]:
        ...

    def to_standard(
        self, 
        code: str,
        ratio: Dict[str, Any]
    ) -> StandardFundamentalIndexSearchResults:
        ...

class IVistockFinancialModelsParser(Protocol):
    def to_query(
        self,
        code: str,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> List[str]:
        ...

    def to_standard(
        self,
        code: str,
        models: List[Dict[str, Any]]
    ) -> StandardFinancialModelsSearchResults:
        ...

class IVistockFinancialStatementsIndexParser(Protocol):
    def to_query(
        self,
        code: str,
        start_year: Optional[int] = None,
        end_year: int = datetime.now().year,
        report: Union[VistockReportTypeCategory, str] = VistockReportTypeCategory.ANNUAL,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> List[str]:
        ...

    def to_standard(
        self,
        models: StandardFinancialModelsSearchResults,
        statements: List[Dict[str, Any]]
    ) -> StandardFinancialStatementsIndexSearchResults:
        ...

class IVistockMarketPricesParser(Protocol):
    def to_query(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        ascending: bool = True
    ) -> List[str]:
        ...

    def to_resolution(
        self, 
        data: List[Dict[str, Any]], 
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY
    ) -> List[Dict[str, Any]]:
        ...

    def to_standard(
        self,
        prices: List[Dict[str, Any]]
    ) -> StandardMarketPricesSearchResults:
        ...

    def to_advanced(
        self,
        prices: List[Dict[str, Any]]
    ) -> AdvancedMarketPricesSearchResults:
        ...

class IVistockChangePricesParser(Protocol):
    def to_query(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL
    ) -> List[str]:
        ...

    def to_standard(
        self,
        prices: List[Dict[str, Any]]
    ) -> StandardChangePricesSearchResults:
        ...

class IVistockStockListingParser(Protocol):
    def to_query(
        self,
        industry: Union[VistockIndustryCategory, str] = VistockIndustryCategory.ALL,
        floor: Union[VistockFloorCategory, str] = VistockFloorCategory.ALL,
        company_type: Union[VistockCompanyTypeCategory, str] = VistockCompanyTypeCategory.ALL,
        letter: Union[VistockLetterCategory, str] = VistockLetterCategory.ALL
    ) -> str:
        ...

    def to_standard(
        self,
        data: List[Dict[str, Any]]
    ) -> StandardStockListingSearchResults:
        ...

class IVistockTradingIndexParser(Protocol):
    def to_payload(
        self,
        code: str,
        current_datetime: str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    ) -> Dict[str, Any]:
        ...

    def to_standard(
        self,
        data: List[Dict[str, Any]]
    ) -> StandardTradingIndexSearchResults:
        ...