from vistock.core.interfaces.ivistockparser import IVistockTradingIndexParser
from vistock.core.models import (
    StandardTradingIndexSearch,
    StandardTradingIndexSearchResults
)
from vistock.core.utils import (
    VistockValidator,
    VistockConverter
)
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

class VistockDNSETradingIndexParser(IVistockTradingIndexParser):
    def to_payload(
        self,
        code: str,
        current_datetime: str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    ) -> Dict[str, Any]:
        if not VistockValidator.validate_code(code=code):
            raise ValueError(
                'Invalid code: "code" must be a non-empty alphanumeric string with exactly 3 characters representing the stock code. Please ensure that the code is specified correctly.'
            )
        
        dt = datetime.strptime(current_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')

        if dt.weekday() == 5:
            dt -= timedelta(days=1)
        elif dt.weekday() == 6:
            dt -= timedelta(days=2)

        date = dt.strftime('%Y-%m-%d')
        current_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        return {
            "operationName": "GetKrxTicksBySymbols",
            "query": f"""
                query GetKrxTicksBySymbols {{
                    GetKrxTicksBySymbols(
                        symbols: "{code}", 
                        date: "{date}", 
                        limit: 100000, 
                        before: "{current_datetime}", 
                        board: 2
                    ) {{
                        ticks {{
                            symbol
                            matchPrice
                            matchQtty
                            sendingTime
                            side
                        }}
                    }}
                }}
            """,
            "variables": {}
        }
    
    def to_standard(
        self,
        data: List[Dict[str, Any]]
    ) -> StandardTradingIndexSearchResults:
        return StandardTradingIndexSearchResults(
            results=[
                StandardTradingIndexSearch(
                    code=item.get('symbol', ''),
                    match_price=item.get('matchPrice', 0.0),
                    match_volume= item.get('matchQtty', 0),
                    sending_time=VistockConverter.from_utc_to_local(item.get('sendingTime', '')),
                    side=item.get('side', 0)
                ) for item in data
            ],
            total_results=len(data)
        )