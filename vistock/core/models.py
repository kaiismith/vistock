from pydantic import BaseModel
from typing import List

class StandardVnDirectStockIndex(BaseModel):
    code: str
    date: str
    time: str
    tfloor: str
    type: str
    mopen: float
    mhigh: float
    mlow: float
    mclose: float
    maverage: float
    nmvolume: int

    def __repr__(self):
        return super().__repr__()

class AdvancedVnDirectStockIndex(BaseModel):
    standard: StandardVnDirectStockIndex
    basic: float
    ceiling: float
    floor: float
    open: float
    high: float
    low: float
    close: float
    average: float
    nmvalue: float
    ptvolume: float
    ptvalue: float
    change: float
    mchange: float
    pctchange: float

    def __repr__(self):
        return super().__repr__()

class StandardVnDirectStockIndexSearchResults(BaseModel):
    results: List[StandardVnDirectStockIndex]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'

class AdvancedVnDirectStockIndexSearchResults(BaseModel):
    results: List[AdvancedVnDirectStockIndex]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'

class StandardVnDirectFundamentalIndexSearchResults(BaseModel):
    marketcap: float
    nm_volume_avg_cr_10d: float
    price_highest_cr_52w: float
    price_lowest_cr_52w: float
    outstanding_shares: float
    freefloat: float
    beta: float
    price_to_earnings: float
    price_to_book: float
    roae_tr_avg_5q: float
    roaa_tr_avg_5q: float
    dividend_yield: float
    eps_tr: float
    bvps_cr: float

    def __str__(self):
        fields = ', '.join(f"{k}={v!r}" for k, v in self.model_dump().items())
        return f'{self.__class__.__name__}({fields})'
    
class Standard24HMoneyStockSection(BaseModel):
    code: str
    company_name: str
    tfloor: str
    company_type: str
    icb_name_vi: str
    icb_name_en: str
    listed_share_vol: int
    fiingroup_icb_code: int

    def __repr__(self):
        return super().__repr__()

class Standard24HMoneyStockSectionSearchResults(BaseModel):
    results: List[Standard24HMoneyStockSection]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
