from vistock.core.constants import (
    DEFAULT_VNDIRECT_STOCK_INDEX_START_DATE,
    DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_START_YEAR,
    DEFAULT_VNDIRECT_STOCK_INDEX_LIMIT,
    DEFAULT_VNDIRECT_FINANCIAL_MODELS_LIMIT,
    DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_LIMIT,
    DEFAULT_VNDIRECT_MARKET_PRICES_START_DATE,
    DEFAULT_VNDIRECT_MARKET_PRICES_LIMIT
)
from vistock.core.interfaces.ivistockparser import (
    IVistockStockIndexParser,
    IVistockFundamentalIndexParser,
    IVistockFinancialModelsParser,
    IVistockFinancialStatementsIndexParser,
    IVistockMarketPricesParser,
    IVistockChangePricesParser
)
from vistock.core.utils import (
    VistockValidator, 
    VistockConverter,
    VistockNormalizator,
    VistockGenerator
)
from vistock.core.enums import (
    VistockResolutionCode,
    VistockFinancialModelsCategory,
    VistockReportTypeCategory,
    VistockIndexCode,
    VistockPeriodCode
)
from vistock.core.models import (
    StandardStockIndexSearch,
    StandardStockIndexSearchResults,
    AdvancedStockIndexSearch,
    AdvancedStockIndexSearchResults,
    StandardFundamentalIndexSearchResults,
    StandardFinancialModelsSearch,
    StandardFinancialModelsSearchResults,
    StandardFinancialStatementsIndex,
    StandardFinancialStatementsIndexSearchResults,
    StandardMarketPricesSearch,
    StandardMarketPricesSearchResults,
    AdvancedMarketPricesSearch,
    AdvancedMarketPricesSearchResults,
    StandardChangePricesSearch,
    StandardChangePricesSearchResults
)
from typing import List, Dict, Any, Union, Optional, DefaultDict
from collections import defaultdict
from urllib.parse import urlencode
from datetime import datetime

class VistockVndirectStockIndexParser(IVistockStockIndexParser):
    def to_query(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d')
    ) -> str:
        if not VistockValidator.validate_code(code=code):
            raise ValueError(
                'Invalid code: "code" must be a non-empty alphanumeric string with exactly 3 characters representing the stock code. Please ensure that the code is specified correctly.'
            )
        
        query = [f'code:{code}']

        if not start_date:
            start_date = DEFAULT_VNDIRECT_STOCK_INDEX_START_DATE

        if not VistockValidator.validate_date_format(date=start_date):
            raise ValueError(
                f'Invalid start date format: "{start_date}". The start date must be in the "YYYY-MM-DD" format to ensure proper parsing and validation.'
            )
        
        if not VistockValidator.validate_date_format(date=end_date):
            raise ValueError(
                f'Invalid end date format: "{end_date}". The end date must be in the "YYYY-MM-DD" format to ensure proper parsing and validation.'
            )
        
        if not VistockValidator.validate_date_range(start_date=start_date, end_date=end_date):
            raise ValueError(
                'Invalid date range: "start_date" must be earlier than "end_date". Please ensure that the start date precedes the end date to maintain a valid chronological order.'
            )
        
        query.append(f'date:gte:{start_date}')
        query.append(f'date:lte:{end_date}')

        q = '~'.join(query)

        params: Dict[str, Any] = {
            'sort': 'date',
            'q': q,
            'size': DEFAULT_VNDIRECT_STOCK_INDEX_LIMIT,
            'page': 1
        }

        return f'?{urlencode(params)}'
    
    def to_resolution(
        self, 
        data: List[Dict[str, Any]], 
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY
    ) -> List[Dict[str, Any]]:
        if not VistockValidator.validate_enum_value(resolution, VistockResolutionCode):
            raise ValueError(
                f'Invalid resolution: "{resolution}". The resolution must be one of the predefined values: {", ".join([r.value for r in VistockResolutionCode])}. Please ensure that the resolution is specified correctly.'
            )
        resolution = VistockNormalizator.to_enum(resolution, VistockResolutionCode)

        if resolution == VistockResolutionCode.DAY or resolution == VistockResolutionCode.TICK:
            return data
        
        grouped: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        buckets : DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)

        for item in data:
            bucket_key = VistockConverter.from_date_to_dateresolution(item.get('date', ''), resolution)
            buckets[bucket_key].append(item)

        for _, items in buckets.items():
            sorted_items = sorted(items, key=lambda x: x['date'])
            key = sorted_items[0].get('date', '')
            grouped[key] = sorted_items

        results: List[Dict[str, Any]] = []
        for key, items in grouped.items():
            mopen = items[0].get('adOpen', 0.0)
            mhigh = max(item.get('adHigh', 0.0) for item in items)
            mlow = min(item.get('adLow', 0.0) for item in items)
            mclose = items[-1].get('adClose', 0.0)
            nmvolume = sum(item.get('nmVolume', 0) for item in items)

            results.append({
                'code': items[0].get('code', ''),
                'date': key,
                'floor': items[0].get('floor', ''),
                'adOpen': mopen,
                'adHigh': mhigh,
                'adLow': mlow,
                'adClose': mclose,
                'nmVolume': nmvolume
            })

        return results
    
    def to_standard(self, data: List[Dict[str, Any]]) -> StandardStockIndexSearchResults:
        return StandardStockIndexSearchResults(
            results=[
                StandardStockIndexSearch(
                    code=item.get('code', ''),
                    date=item.get('date', ''),
                    tfloor=item.get('floor', ''),
                    mopen=item.get('adOpen', 0.0),
                    mhigh=item.get('adHigh', 0.0),
                    mlow=item.get('adLow', 0.0),
                    mclose=item.get('adClose', 0.0),
                    nmvolume=int(item.get('nmVolume', 0))
                ) for item in data
            ],
            total_results=len(data)
        )
    
    def to_advanced(self, data: List[Dict[str, Any]]) -> AdvancedStockIndexSearchResults:
        return AdvancedStockIndexSearchResults(
            results=[
                AdvancedStockIndexSearch(
                    code=item.get('code', ''),
                    date=item.get('date', ''),
                    tfloor=item.get('floor', ''),
                    basic=item.get('basicPrice', 0.0),
                    ceiling=item.get('ceilingPrice', 0.0),
                    floor=item.get('floorPrice', 0.0),
                    open=item.get('open', 0.0),
                    high=item.get('high', 0.0),
                    low=item.get('low', 0.0),
                    close=item.get('close', 0.0),
                    average=item.get('average', 0.0),
                    mopen=item.get('adOpen', 0.0),
                    mhigh=item.get('adHigh', 0.0),
                    mlow=item.get('adLow', 0.0),
                    mclose=item.get('adClose', 0.0),
                    maverage=item.get('adAverage', 0.0),
                    nmvolume=int(item.get('nmVolume', 0)),
                    nmvalue=item.get('nmValue', 0.0),
                    ptvolume=item.get('ptVolume', 0.0),
                    ptvalue=item.get('ptValue', 0.0),
                    change=item.get('change', 0.0),
                    mchange=item.get('adChange', 0.0),
                    pctchange=item.get('pctChange', 0.0),
                )
                for item in data
            ],
            total_results=len(data)
        )
    
class VistockVndirectFundamentalIndexParser(IVistockFundamentalIndexParser):
    def __init__(self):
        self._queries = [
            '?filter=ratioCode:MARKETCAP,NMVOLUME_AVG_CR_10D,PRICE_HIGHEST_CR_52W,PRICE_LOWEST_CR_52W,OUTSTANDING_SHARES,FREEFLOAT,BETA,PRICE_TO_EARNINGS,PRICE_TO_BOOK,DIVIDEND_YIELD,BVPS_CR,&where=code:{code}&order=reportDate&fields=ratioCode,value',
            '?filter=ratioCode:ROAE_TR_AVG5Q,ROAA_TR_AVG5Q,EPS_TR,&where=code:{code}&order=reportDate&fields=ratioCode,value'
        ]

    def to_query(self, code: str) -> List[str]:
        if not VistockValidator.validate_code(code=code):
            raise ValueError(
                'Invalid code: "code" must be a non-empty alphanumeric string with exactly 3 characters representing the stock code. Please ensure that the code is specified correctly.'
            )
        
        return [query.format(code=code) for query in self._queries]
    
    def to_standard(
        self,
        code: str,
        ratio: Dict[str, Any]
    ) -> StandardFundamentalIndexSearchResults:
        return StandardFundamentalIndexSearchResults(
            code=code,
            date=datetime.now().strftime('%Y-%m-%d'),
            marketcap=ratio.get("MARKETCAP", 0.0),
            nmvolume_avg_cr_10d=ratio.get("NMVOLUME_AVG_CR_10D", 0.0),
            price_highest_cr_52w=ratio.get("PRICE_HIGHEST_CR_52W", 0.0),
            price_lowest_cr_52w=ratio.get("PRICE_LOWEST_CR_52W", 0.0),
            outstanding_shares=ratio.get("OUTSTANDING_SHARES", 0.0),
            freefloat=ratio.get("FREEFLOAT", 0.0),
            beta=ratio.get("BETA", 0.0),
            price_to_earnings=ratio.get("PRICE_TO_EARNINGS", 0.0),
            price_to_book=ratio.get("PRICE_TO_BOOK", 0.0),
            roae_tr_avg5q=ratio.get("ROAE_TR_AVG5Q", 0.0),
            roaa_tr_avg5q=ratio.get("ROAA_TR_AVG5Q", 0.0),
            dividend_yield=ratio.get("DIVIDEND_YIELD", 0.0),
            eps_tr=ratio.get("EPS_TR", 0.0),
            bvps_cr=ratio.get("BVPS_CR", 0.0),
        )
    
class VistockVndirectFinancialModelsParser(IVistockFinancialModelsParser):
    def __init__(self):
        self._query = '?sort=displayOrder:asc&q=codeList:{code}~modelType:{model}~note:TT199/2014/TT-BTC,TT334/2016/TT-BTC,TT49/2014/TT-NHNN,TT202/2014/TT-BTC~displayLevel:0,1,2,3&size={limit}'
    
    def to_query(
        self,
        code: str,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> List[str]:
        if not VistockValidator.validate_code(code=code):
            raise ValueError(
                'Invalid code: "code" must be a non-empty alphanumeric string with exactly 3 characters representing the stock code. Please ensure that the code is specified correctly.'
            )
        
        if not VistockValidator.validate_enum_value(model, VistockFinancialModelsCategory):
            raise ValueError(
                f'Invalid model: "{model}". The model must be one of the predefined values: {", ".join([r.value for r in VistockFinancialModelsCategory])}. Please ensure that the model is specified correctly.'
            )
        model = VistockNormalizator.to_enum(model, VistockFinancialModelsCategory)
        
        queries: List[str] = []

        if model != VistockFinancialModelsCategory.ALL:
            query = self._query.format(
                code=code,
                model=VistockNormalizator.to_string(model, VistockFinancialModelsCategory),
                limit=DEFAULT_VNDIRECT_FINANCIAL_MODELS_LIMIT
            )
            queries.append(f'{query}')

            return queries

        for category in VistockFinancialModelsCategory:
            if category == VistockFinancialModelsCategory.ALL:
                continue

            query = self._query.format(
                code=code,
                model=category.value,
                limit=DEFAULT_VNDIRECT_FINANCIAL_MODELS_LIMIT
            )
            queries.append(f'{query}')

        return queries

    def to_standard(
        self,
        code: str,
        models: List[Dict[str, Any]]
    ) -> StandardFinancialModelsSearchResults:
        return StandardFinancialModelsSearchResults(
            results=[
                StandardFinancialModelsSearch(
                    code=code,
                    date=datetime.now().strftime('%Y-%m-%d'),
                    model_type=item.get('modelType', 0),
                    model_type_name=item.get('modelTypeName', ''),
                    model_vn_desc=item.get('modelVnDesc', ''),
                    model_en_desc=item.get('modelEnDesc', ''),
                    company_form=item.get('companyForm', ''),
                    note=item.get('note', ''),
                    item_code=item.get('itemCode', 0),
                    item_vn_name=item.get('itemVnName', ''),
                    item_en_name=item.get('itemEnName', ''),
                    display_order=item.get('displayOrder', 0),
                    display_level=item.get('displayLevel', 0),
                    form_type=item.get('formType', '')
                ) for item in models
            ],
            total_results=len(models)
        )
    
class VistockVndirectFinancialStatementsIndexParser(IVistockFinancialStatementsIndexParser):
    def __init__(self):
        self._query = '?q=code:{code}~reportType:{report}~modelType:{model}~fiscalDate:{fiscal_date}&sort=fiscalDate&size={limit}'

    def to_query(
        self,
        code: str,
        start_year: Optional[int] = None,
        end_year: int = datetime.now().year,
        report: Union[VistockReportTypeCategory, str] = VistockReportTypeCategory.ANNUAL,
        model: Union[VistockFinancialModelsCategory, str] = VistockFinancialModelsCategory.ALL
    ) -> List[str]:
        if not VistockValidator.validate_code(code=code):
            raise ValueError(
                'Invalid code: "code" must be a non-empty alphanumeric string with exactly 3 characters representing the stock code. Please ensure that the code is specified correctly.'
            )
        
        if not start_year:
            start_year = DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_START_YEAR
        
        if not VistockValidator.validate_year(year=start_year):
            raise ValueError(
                f'Invalid start year: {start_year}. The start year cannot be later than {datetime.now().year}.'
            )
        
        if not VistockValidator.validate_year(year=end_year):
            raise ValueError(
                f'Invalid end year: {end_year}. The end year cannot be later than {datetime.now().year}.'
            )
        
        if not VistockValidator.validate_year_range(start_year=start_year, end_year=end_year):
            raise ValueError(
                'Invalid year range: "start_year" must be earlier than or equal to "end_year". Please ensure that the start year precedes or is equal to the end year to maintain a valid chronological order.'
            )
        
        if not VistockValidator.validate_enum_value(report, VistockReportTypeCategory):
            raise ValueError(
                f'Invalid report: "{report}". The report must be one of the predefined values: {", ".join([r.value for r in VistockReportTypeCategory])}. Please ensure that the report is specified correctly.'
            )
        report = VistockNormalizator.to_enum(report, VistockReportTypeCategory)

        if not VistockValidator.validate_enum_value(model, VistockFinancialModelsCategory):
            raise ValueError(
                f'Invalid model: "{model}". The model must be one of the predefined values: {", ".join([r.value for r in VistockFinancialModelsCategory])}. Please ensure that the model is specified correctly.'
            )
        model = VistockNormalizator.to_enum(model, VistockFinancialModelsCategory)
        
        match report:
            case VistockReportTypeCategory.ANNUAL:
                fiscal_date = VistockGenerator.generate_annual_dates(
                    start_year=start_year, 
                    end_year=end_year
                )
            case VistockReportTypeCategory.QUARTER:
                fiscal_date = VistockGenerator.generate_quarterly_dates(
                    start_year=start_year,
                    end_year=end_year
                )
            
        queries: List[str] = []

        if model != VistockFinancialModelsCategory.ALL:
            query = self._query.format(
                code=code,
                report=VistockNormalizator.to_string(report, VistockReportTypeCategory),
                model=VistockNormalizator.to_string(model, VistockFinancialModelsCategory),
                fiscal_date=fiscal_date,
                limit=DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_LIMIT
            )
            queries.append(f'{query}')

            return queries

        for category in VistockFinancialModelsCategory:
            if category == VistockFinancialModelsCategory.ALL:
                continue

            query = self._query.format(
                code=code,
                report=VistockNormalizator.to_string(report, VistockReportTypeCategory),
                model=category.value,
                fiscal_date=fiscal_date,
                limit=DEFAULT_VNDIRECT_FINANCIAL_STATEMENTS_LIMIT
            )
            queries.append(f'{query}')

        return queries
    
    def to_standard(
        self,
        models: StandardFinancialModelsSearchResults,
        statements: List[Dict[str, Any]]
    ) -> StandardFinancialStatementsIndexSearchResults:
        return StandardFinancialStatementsIndexSearchResults(
            results=[
                StandardFinancialStatementsIndex(
                    code=statement.get('code', ''),
                    date=model.date,
                    model_type=model.model_type,
                    model_type_name=model.model_type_name,
                    model_vn_desc=model.model_vn_desc,
                    model_en_desc=model.model_en_desc,
                    company_form=model.company_form,
                    note=model.note,
                    item_code=model.item_code,
                    item_vn_name=model.item_vn_name,
                    item_en_name=model.item_en_name,
                    display_order=model.display_order,
                    display_level=model.display_level,
                    form_type=model.form_type,
                    report_type=statement.get('reportType', ''),
                    numeric_value=statement.get('numericValue', 0.0),
                    fiscal_date=statement.get('fiscalDate', ''),
                    created_date=statement.get('createdDate', ''),
                    modified_date=statement.get('modifiedDate', '')
                )
                for model in models.results
                for statement in statements
                if statement.get('modelType') == model.model_type
                and statement.get('itemCode') == model.item_code
            ],
            total_results=len([
                1
                for model in models.results
                for statement in statements
                if statement.get('modelType') == model.model_type
                and statement.get('itemCode') == model.item_code
            ])
        )
    
class VistockVndirectMarketPricesParser(IVistockMarketPricesParser):
    def __init__(self):
        self._query = '?sort=date:{order}&size={limit}&q=code:{code}~date:gte:{start_date}'

    def to_query(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        start_date: Optional[str] = None,
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        ascending: bool = True
    ) -> List[str]:
        if not VistockValidator.validate_enum_value(code, VistockIndexCode):
            raise ValueError(
                f'Invalid code: "{code}". The code must be one of the predefined values: {", ".join([r.value for r in VistockIndexCode])}. Please ensure that the code is specified correctly.'
            )
        code = VistockNormalizator.to_enum(code, VistockIndexCode)

        if not start_date:
            start_date = DEFAULT_VNDIRECT_MARKET_PRICES_START_DATE

        if not VistockValidator.validate_date_format(date=start_date):
            raise ValueError(
                f'Invalid start date format: "{start_date}". The start date must be in the "YYYY-MM-DD" format to ensure proper parsing and validation.'
            )
        
        if not VistockValidator.validate_date_format(date=end_date):
            raise ValueError(
                f'Invalid end date format: "{end_date}". The end date must be in the "YYYY-MM-DD" format to ensure proper parsing and validation.'
            )
        
        if not VistockValidator.validate_date_range(start_date=start_date, end_date=end_date):
            raise ValueError(
                'Invalid date range: "start_date" must be earlier than "end_date". Please ensure that the start date precedes the end date to maintain a valid chronological order.'
            )
        
        order = 'asc' if ascending else 'desc'
        
        queries: List[str] = []
            
        if code != VistockIndexCode.ALL:
            query = self._query.format(
                code=VistockNormalizator.to_string(code, VistockIndexCode),
                start_date=start_date,
                order=order,
                limit=DEFAULT_VNDIRECT_MARKET_PRICES_LIMIT
            )
            queries.append(f'{query}')

            return queries

        for idxcode in VistockIndexCode:
            if idxcode == VistockIndexCode.ALL or idxcode == VistockIndexCode.VN30F1M:
                continue

            query = self._query.format(
                code=idxcode.value,
                start_date=start_date,
                order=order,
                limit=DEFAULT_VNDIRECT_MARKET_PRICES_LIMIT
            )
            queries.append(query)

        return queries
        
    def to_resolution(
        self, 
        data: List[Dict[str, Any]], 
        resolution: Union[VistockResolutionCode, str] = VistockResolutionCode.DAY
    ) -> List[Dict[str, Any]]:
        if not VistockValidator.validate_enum_value(resolution, VistockResolutionCode):
            raise ValueError(
                f'Invalid resolution: "{resolution}". The resolution must be one of the predefined values: {", ".join([r.value for r in VistockResolutionCode])}. Please ensure that the resolution is specified correctly.'
            )
        resolution = VistockNormalizator.to_enum(resolution, VistockResolutionCode)

        if resolution == VistockResolutionCode.DAY or resolution == VistockResolutionCode.TICK:
            return data
        
        grouped: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        buckets : DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)

        for item in data:
            bucket_key = VistockConverter.from_date_to_dateresolution(item.get('date', ''), resolution)
            buckets[bucket_key].append(item)

        for _, items in buckets.items():
            sorted_items = sorted(items, key=lambda x: x['date'])
            key = sorted_items[0].get('date', '')
            grouped[key] = sorted_items

        results: List[Dict[str, Any]] = []
        for key, items in grouped.items():
            open = items[0].get('open', 0.0)
            high = max(item.get('high', 0.0) for item in items)
            low = min(item.get('low', 0.0) for item in items)
            close = items[-1].get('close', 0.0)
            nmvolume = sum(item.get('nmVolume', 0) for item in items)

            results.append({
                'code': items[0].get('code', ''),
                'date': key,
                'floor': items[0].get('floor', ''),
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'nmVolume': nmvolume
            })

        return results
    
    def to_standard(
        self,
        prices: List[Dict[str, Any]]
    ) -> StandardMarketPricesSearchResults:
        return StandardMarketPricesSearchResults(
            results=[
                StandardMarketPricesSearch(
                    code=item.get('code', ''),
                    date=item.get('date', ''),
                    tfloor=item.get('floor', ''),
                    open=item.get('open', 0.0),
                    high=item.get('high', 0.0),
                    low=item.get('low', 0.0),
                    close=item.get('close', 0.0),
                    nmvolume=item.get('nmVolume', 0.0),
                ) for item in prices
            ],
            total_results=len(prices)
        )

    def to_advanced(
        self,
        prices: List[Dict[str, Any]]
    ) -> AdvancedMarketPricesSearchResults:
        return AdvancedMarketPricesSearchResults(
            results=[
                AdvancedMarketPricesSearch(
                    code=item.get('code', ''),
                    date=item.get('date', ''),
                    time=item.get('time', ''),
                    tfloor=item.get('floor', ''),
                    type=item.get('type', ''),
                    open=item.get('open', 0.0),
                    high=item.get('high', 0.0),
                    low=item.get('low', 0.0),
                    close=item.get('close', 0.0),
                    change=item.get('change', 0.0),
                    pct_change=item.get('pctChange', 0.0),
                    accumulated_volume=item.get('accumulatedVol', 0.0),
                    accumulated_value=item.get('accumulatedVal', 0.0),
                    nmvolume=item.get('nmVolume', 0.0),
                    nmvalue=item.get('nmValue', 0.0),
                    ptvolume=item.get('ptVolume', 0.0),
                    ptvalue=item.get('ptValue', 0.0),
                    advances=item.get('advances', 0.0),
                    declines=item.get('declines', 0.0),
                    no_change=item.get('noChange', 0.0),
                    no_trade=item.get('noTrade', 0.0),
                    ceiling_stocks=item.get('ceilingStocks', 0.0),
                    floor_stocks=item.get('floorStocks', 0.0),
                    val_chg_pct_cr1d=item.get('valChgPctCr1D', 0.0)
                ) for item in prices
            ],
            total_results=len(prices)
        )

class VistockVndirectChangePricesParser(IVistockChangePricesParser):
    def __init__(self):
        self._query = '?q=code:{code}~period:{period}'

    def to_query(
        self,
        code: Union[VistockIndexCode, str] = VistockIndexCode.ALL,
        period: Union[VistockPeriodCode, str] = VistockPeriodCode.ALL
    ) -> List[str]:
        if not VistockValidator.validate_enum_value(code, VistockIndexCode):
            raise ValueError(
                f'Invalid code: "{code}". The code must be one of the predefined values: {", ".join([r.value for r in VistockIndexCode])}. Please ensure that the code is specified correctly.'
            )
        code = VistockNormalizator.to_string(code, VistockIndexCode)

        if code == 'ALL':
            code = 'VNINDEX,HNX,UPCOM,VN30,VN30F1M'

        if not VistockValidator.validate_enum_value(period, VistockPeriodCode):
            raise ValueError(
                f'Invalid period: "{period}". The period must be one of the predefined values: {", ".join([r.value for r in VistockPeriodCode])}. Please ensure that the period is specified correctly.'
            )
        period = VistockNormalizator.to_enum(period, VistockPeriodCode)

        queries: List[str] = []

        if period != VistockPeriodCode.ALL:
            query = self._query.format(
                code=code,
                period=VistockNormalizator.to_string(period, VistockPeriodCode)
            )
            queries.append(f'{query}')

            return queries

        for period in VistockPeriodCode:
            if period == VistockPeriodCode.ALL:
                continue

            query = self._query.format(
                code=code,
                period=period.value
            )
            queries.append(f'{query}')

        return queries

    def to_standard(
        self,
        prices: List[Dict[str, Any]]
    ) -> StandardChangePricesSearchResults:
        return StandardChangePricesSearchResults(
            results=[
                StandardChangePricesSearch(
                    code=item.get('code', ''),
                    name=item.get('name', ''),
                    type=item.get('type', ''),
                    period=item.get('period', ''),
                    price=item.get('price', 0.0),
                    bop_price=item.get('bopPrice', 0.0),
                    change=item.get('change', 0.0),
                    pct_change=item.get('changePct', 0.0),
                    last_updated=item.get('lastUpdated', '')
                ) for item in prices
            ],
            total_results=len(prices)
        )
           