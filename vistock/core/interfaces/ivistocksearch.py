from vistock.core.models import StandardVnDirectStockIndex, AdvancedVnDirectStockIndex
from typing import List, Union, Protocol, Literal
from datetime import datetime

class IVistockVnDirectSearch(Protocol):
    def search(
        self, 
        code: str,
        start_date: str = '2012-01-01',
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        resolution: Literal['day', 'week', 'month', 'year'] = 'day',
        advanced: bool = True,
        ascending: bool = False
    ) -> Union[List[StandardVnDirectStockIndex], List[AdvancedVnDirectStockIndex]]:
        ...

class AsyncIVistockVnDirectSearch(Protocol):
    async def search(
        self, 
        code: str,
        start_date: str = '2012-01-01',
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        resolution: Literal['day', 'week', 'month', 'year'] = 'day',
        advanced: bool = True,
        ascending: bool = False
    ) -> Union[List[StandardVnDirectStockIndex], List[AdvancedVnDirectStockIndex]]:
        ...