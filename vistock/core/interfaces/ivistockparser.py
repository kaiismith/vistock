from datetime import datetime
from typing import Protocol

class IViStockVnDirectParser(Protocol):
    def parse_url_path(
        self,
        code: str,
        start_date: str = '2012-01-01',
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        limit: int = 1
    ) -> str:
        ...

class IVistock24HMoneyParser(Protocol):
    def parse_url_path(
        self,
        industry_code: str = 'all',
        floor_code: str = 'all',
        company_type: str = 'all',
        letter: str = 'all',
        limit: int = 2000
    ) -> str:
        ...
    