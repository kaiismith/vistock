from typing import List, Optional
from pydantic import BaseModel

class StandardStockIndexSearch(BaseModel):
    code: str
    date: str
    tfloor: str
    mopen: float
    mhigh: float
    mlow: float
    mclose: float
    nmvolume: int

    def __repr__(self):
        return super().__repr__()
    
class StandardStockIndexSearchResults(BaseModel):
    results: List[StandardStockIndexSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
    
class AdvancedStockIndexSearch(BaseModel):
    code: str
    date: str
    tfloor: str
    basic: float
    ceiling: float
    floor: float
    open: float
    high: float
    low: float
    close: float
    average: float
    mopen: float
    mhigh: float
    mlow: float
    mclose: float
    maverage: float
    nmvolume: int
    nmvalue: int
    ptvolume: float
    ptvalue: float
    change: float
    mchange: float
    pctchange: float

class AdvancedStockIndexSearchResults(BaseModel):
    results: List[AdvancedStockIndexSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
    
class StandardFundamentalIndexSearchResults(BaseModel):
    code: str
    date: str
    marketcap: float
    nmvolume_avg_cr_10d: float
    price_highest_cr_52w: float
    price_lowest_cr_52w: float
    outstanding_shares: float
    freefloat: float
    beta: float
    price_to_earnings: float
    price_to_book: float
    roae_tr_avg5q: float
    roaa_tr_avg5q: float
    dividend_yield: float
    eps_tr: float
    bvps_cr: float

    def __repr__(self):
        return super().__repr__()
    
class StandardFinancialModelsSearch(BaseModel):
    code: str
    date: str
    model_type: int
    model_type_name: str
    model_vn_desc: str
    model_en_desc: str
    company_form: str
    note: str
    item_code: int
    item_vn_name: str
    item_en_name: str
    display_order: int
    display_level: int
    form_type: str 

    def __repr__(self):
        return super().__repr__()

class StandardFinancialModelsSearchResults(BaseModel):
    results: List[StandardFinancialModelsSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
    
class StandardFinancialStatementsIndex(BaseModel):
    code: str
    date: str
    model_type: int
    model_type_name: str
    model_vn_desc: str
    model_en_desc: str
    company_form: str
    note: str
    item_code: int
    item_vn_name: str
    item_en_name: str
    display_order: int
    display_level: int
    form_type: str 
    report_type: str
    numeric_value: int
    fiscal_date: str
    created_date: str
    modified_date: str

    def __repr__(self):
        return super().__repr__()
    
class StandardFinancialStatementsIndexSearchResults(BaseModel):
    results: List[StandardFinancialStatementsIndex]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'   
    
class StandardMarketPricesSearch(BaseModel):
    code: str
    date: str
    tfloor: str
    open: float
    high: float
    low: float
    close: float
    nmvolume: float

    def __repr__(self):
        return super().__repr__()
    
class StandardMarketPricesSearchResults(BaseModel):
    results: List[StandardMarketPricesSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'

class AdvancedMarketPricesSearch(BaseModel):
    code: str
    date: str
    time: str
    tfloor: str
    type: str
    open: float
    high: float
    low: float
    close: float
    change: float
    pct_change: float
    accumulated_volume: float
    accumulated_value: float
    nmvolume: float
    nmvalue: float
    ptvolume: float
    ptvalue: float
    advances: float
    declines: float
    no_change: float
    no_trade: float
    ceiling_stocks: float
    floor_stocks: float
    val_chg_pct_cr1d: float
    
    def __repr__(self):
        return super().__repr__()

class AdvancedMarketPricesSearchResults(BaseModel):
    results: List[AdvancedMarketPricesSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
        
class StandardChangePricesSearch(BaseModel):
    code: str
    name: str
    type: str
    period: str
    price: float
    bop_price: float
    change: float
    pct_change: float
    last_updated: str

    def __repr__(self):
        return super().__repr__()
    
class StandardChangePricesSearchResults(BaseModel):
    results: List[StandardChangePricesSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
    
class StandardStockListingSearch(BaseModel):
    code: str
    company_name: str
    tfloor: str
    company_type: Optional[str] = ''
    icb_name_vi: Optional[str] = ''
    listed_share_vol: Optional[int] = 0
    fiingroup_icb_code: int

    def __repr__(self):
        return super().__repr__()
    
class StandardStockListingSearchResults(BaseModel):
    results: List[StandardStockListingSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'

class StandardTradingIndexSearch(BaseModel):
    code: str
    match_price: float
    match_volume: int
    sending_time: str
    side: int

    def __repr__(self):
        return super().__repr__()
    
class StandardTradingIndexSearchResults(BaseModel):
    results: List[StandardTradingIndexSearch]
    total_results: int

    def __str__(self):
        results_repr = ', '.join(repr(r) for r in self.results)
        return f'{self.__class__.__name__}(results=[{results_repr}], total_results={self.total_results})'
