
# VnDirect Stock Index Search Guide

## Overview

This stock index search function allows you to programmatically retrieve historical stock index data for Vietnamese stocks. It supports both synchronous and asynchronous usage, and provides options for basic or advanced data output. This guide covers what each parameter means, and how to handle the results.

You can use this search function to:
- Fetch daily historical prices for a given stock code.
- Choose between standard and advanced result formats.
- Sort results by date.
- Save results to a JSON file for further analysis.

## Interfaces

```python
class IVistockVnDirectStockIndexSearch(Protocol):
    def search(
        self, 
        code: str,
        start_date: str = '2012-01-01',
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        resolution: Literal['day'] = 'day',
        advanced: bool = True,
        ascending: bool = False
    ) -> Union[StandardVnDirectStockIndexSearchResults, AdvancedVnDirectStockIndexSearchResults]:
        ...
```

```python
class AsyncIVistockVnDirectStockIndexSearch(Protocol):
    async def async_search(
        self, 
        code: str,
        start_date: str = '2012-01-01',
        end_date: str = datetime.now().strftime('%Y-%m-%d'),
        resolution: Literal['day'] = 'day',
        advanced: bool = True,
        ascending: bool = False
    ) -> Union[StandardVnDirectStockIndexSearchResults, AdvancedVnDirectStockIndexSearchResults]:
        ...
```

### Parameters


- **code** (`str`): The stock code to query (e.g., 'ACB', 'CEO'). This identifies the stock or index you want to retrieve data for.
- **start_date** (`str`, default `'2012-01-01'`): The first date to include in the results, in `YYYY-MM-DD` format.
- **end_date** (`str`, default to today): The last date to include in the results, in `YYYY-MM-DD` format. Defaults to the current date.
- **resolution** (`Literal['day']`, default `'day'`): The time interval for the data. Currently, only daily data is supported.
- **advanced** (`bool`, default `True`): If `True`, returns a more detailed result structure. If `False`, returns a standard summary.
- **ascending** (`bool`, default `False`): If `True`, results are sorted from oldest to newest. If `False`, newest results come first.

### Returns

- Returns a result object: `StandardVnDirectStockIndexSearchResults` (if `advanced=False`) or `AdvancedVnDirectStockIndexSearchResults` (if `advanced=True`). These objects can be converted to a dictionary using `.model_dump()` for serialization.

### Example Usage

#### Importing and Searching

```python
from vistock.modules.vndirect.search import VistockVnDirectStockIndexSearch
import json

async def main():
    vndirect = VistockVnDirectStockIndexSearch()

    data = vndirect.search(
        code="ACB",
        start_date="2025-06-27",
        end_date="2025-06-27",
        resolution="day",
        advanced=True,
        ascending=True
    )

    data = vndirect.async_search(
        code="ACB",
        start_date="2025-06-27",
        end_date="2025-06-27",
        resolution="day",
        advanced=True,
        ascending=True
    )

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data.model_dump(), file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Sample Output (`advanced=True`)
```json
{
  "results": [
    {
      "standard": {
        "code": "ACB",
        "date": "2025-06-27",
        "time": "15:06:02",
        "tfloor": "HOSE",
        "type": "STOCK",
        "mopen": 21.3,
        "mhigh": 21.3,
        "mlow": 21.15,
        "mclose": 21.2,
        "maverage": 21.206,
        "nmvolume": 6312400
      },
      "basic": 21.2,
      "ceiling": 22.65,
      "floor": 19.75,
      "open": 21.3,
      "high": 21.3,
      "low": 21.15,
      "close": 21.2,
      "average": 21.206,
      "nmvalue": 133863765000.0,
      "ptvolume": 0.0,
      "ptvalue": 0.0,
      "change": 0.0,
      "mchange": 0.0,
      "pctchange": 0.0
    }
  ],
  "total_results": 1
}
```

#### Sample Output (`advanced=False`)

```json
{
  "results": [
    {
      "code": "ACB",
      "date": "2025-06-27",
      "time": "15:06:02",
      "tfloor": "HOSE",
      "type": "STOCK",
      "mopen": 21.3,
      "mhigh": 21.3,
      "mlow": 21.15,
      "mclose": 21.2,
      "maverage": 21.206,
      "nmvolume": 6312400
    }
  ],
  "total_results": 1
}
```
