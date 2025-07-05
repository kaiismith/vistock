from pydantic import BaseModel

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

