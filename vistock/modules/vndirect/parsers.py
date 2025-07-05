from vistock.core.interfaces.ivistockparser import IViStockVnDirectParser
from vistock.core.constants import DEFAULT_VNDIRECT_DOMAIN
from vistock.core.utils import VistockValidator
from urllib.parse import urlencode
from datetime import datetime
from typing import Dict, Any

class VistockVnDirectParser(IViStockVnDirectParser):
    def __init__(self):
        self._domain = DEFAULT_VNDIRECT_DOMAIN

    def parse_url_path(
        self,
        code: str,
        start_date: str = '2012-01-01',
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        limit: int = 1
    ) -> str:
        if limit < 0:
            raise ValueError(
                'Invalid limit: "limit" must be a positive integer greater than zero to ensure proper pagination and data retrieval.'
            )
        
        if limit == 0:
            limit += 1

        query_parts = [f'code:{code}']

        if not VistockValidator.validate_date_range(start_date=start_date, end_date=end_date):
            raise ValueError(
                'Invalid date range: "start_date" must be earlier than "end_date". Please ensure that the start date precedes the end date to maintain a valid chronological order.'
            )

        if VistockValidator.validate_date_format(date_str=start_date):
            query_parts.append(f'date:gte:{start_date}')
            
        if VistockValidator.validate_date_format(date_str=end_date):
            query_parts.append(f'date:lte:{end_date}')

        q_param = '~'.join(query_parts)

        query_params : Dict[str, Any] = {
            'sort': 'date',
            'q': q_param,
            'size': limit,
            'page': 1
        }

        return f'?{urlencode(query_params)}'
    