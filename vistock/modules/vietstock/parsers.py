from vistock.core.interfaces.ivistockparser import IVistockStockIndexParser
from vistock.core.constants import (
    DEFAULT_VIETSTOCK_STOCK_INDEX_START_DATE,
    DEFAULT_VIETSTOCK_STOCK_INDEX_RESOLUTION
)
from vistock.core.models import (
    StandardStockIndexSearch,
    StandardStockIndexSearchResults,
    AdvancedStockIndexSearchResults
)
from vistock.core.enums import (
    VistockResolutionCode
)
from vistock.core.utils import (
    VistockValidator,
    VistockConverter,
    VistockNormalizator
)
from typing import List, Dict, Union, Any, Optional, DefaultDict
from collections import defaultdict
from datetime import datetime

class VistockVietstockStockIndexParser(IVistockStockIndexParser):
    def __init__(self):
        self._query = '?symbol={code}&resolution={resolution}&from={start_timestamp}&to={end_timestamp}&countback=2'

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

        if not start_date:
            start_date = DEFAULT_VIETSTOCK_STOCK_INDEX_START_DATE

        if not VistockValidator.validate_date_format(date=start_date):
            raise ValueError(
                f'Invalid start date format: "{start_date}". The start date must be in the "YYYY-MM-DD" format to ensure proper parsing and validation.'
            )
        start_timestamp = VistockConverter.from_date_to_timestamp(date=start_date)
        
        if not VistockValidator.validate_date_format(date=end_date):
            raise ValueError(
                f'Invalid end date format: "{end_date}". The end date must be in the "YYYY-MM-DD" format to ensure proper parsing and validation.'
            )
        end_timestamp = VistockConverter.from_date_to_timestamp(date=end_date)
        
        if not VistockValidator.validate_date_range(start_date=start_date, end_date=end_date):
            raise ValueError(
                'Invalid date range: "start_date" must be earlier than "end_date". Please ensure that the start date precedes the end date to maintain a valid chronological order.'
            )
        
        return self._query.format(
            code=code,
            resolution=DEFAULT_VIETSTOCK_STOCK_INDEX_RESOLUTION,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
    
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
    
    def to_standard(
        self,
        data: List[Dict[str, Any]]
    ) -> StandardStockIndexSearchResults:
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

    def to_advanced(
        self,
        data: List[Dict[str, Any]]
    ) -> AdvancedStockIndexSearchResults:
        return AdvancedStockIndexSearchResults(
            results=[],
            total_results=0
        )
        
