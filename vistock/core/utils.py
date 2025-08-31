from vistock.core.enums import (
    VistockPeriodCode,
    VistockResolutionCode,
    VistockIndexCode,
    VistockSector
)
from typing import List, Union, Optional, Type, TypeVar
from dateutil.relativedelta import relativedelta
from datetime import datetime
from urllib.parse import urlparse
from tzlocal import get_localzone
from enum import Enum
import pytz
import time

T = TypeVar('T', bound=Enum)

class VistockValidator:
    @staticmethod
    def validate_url(url: str) -> bool:
        try:
            parsed_url = urlparse(url)
            return all([parsed_url.scheme, parsed_url.netloc])
        
        except Exception:
            return False

    @staticmethod
    def validate_url_with_domain(url: str, domain: str) -> bool:
        try:
            parsed_url = urlparse(url)

            if not parsed_url.scheme in ('http', 'https'):
                return False
            
            if not parsed_url.hostname:
                return False
            
            if not parsed_url.hostname.endswith(domain):
                return False

            return True
        
        except Exception:
            return False
        
    @staticmethod
    def validate_date_format(date: str, format: str = '%Y-%m-%d') -> bool:
        try:
            datetime.strptime(date, format)
            return True
        
        except ValueError:
            return False
        
    @staticmethod
    def validate_date_range(
        start_date: str,
        end_date: str,
        format: str = '%Y-%m-%d'
    ) -> bool:
        try:
            start_datetime = datetime.strptime(start_date, format)
            end_datetime = datetime.strptime(end_date, format)

            return start_datetime <= end_datetime

        except ValueError:
            return False

    @staticmethod
    def validate_enum_value(value: Union[str, Enum], enum_cls: Type[Enum]) -> bool:
        if isinstance(value, enum_cls):
            return True

        if isinstance(value, str):
            if value.upper() in enum_cls.__members__:
                return True
            
            if any(member.value == value for member in enum_cls):
                return True

        return False
        
    @staticmethod
    def validate_code(code: str) -> bool:
        try:
            if len(code) == 3:
                return True
            
            return False
        
        except Exception:
            return False
        
    @staticmethod
    def validate_year(year: int) -> bool:
        try:
            return year <= datetime.now().year
        
        except Exception:
            return False
    
    @staticmethod
    def validate_year_range(start_year: int, end_year: int) -> bool:
        try:
            if start_year > end_year:
                return False

            return True

        except Exception:
            return False
        
    @staticmethod
    def validate_index_code(code: str) -> bool:
        return bool(code and code in {item.value for item in VistockIndexCode})
    
    @staticmethod
    def validate_index_period(period: str) -> bool:
        return bool(period and period in {item.value for item in VistockPeriodCode})

class VistockNormalizator:
    @staticmethod
    def to_string(value: Union[str, Enum], enum_cls: Type[Enum]) -> str:
        if isinstance(value, enum_cls):
            return value.value

        if isinstance(value, str):
            if value.upper() in enum_cls.__members__:
                return enum_cls[value.upper()].value
            for member in enum_cls:
                if member.value == value:
                    return value

        raise ValueError(f"Cannot normalize value '{value}' for enum {enum_cls.__name__}")
    
    @staticmethod
    def to_enum(value: Union[str, Enum], enum_cls: Type[T]) -> T:
        if isinstance(value, enum_cls):
            return value

        if isinstance(value, str):
            if value.upper() in enum_cls.__members__:
                return enum_cls[value.upper()]
            
            for member in enum_cls:
                if member.value == value:
                    return member

        raise ValueError(f"Cannot normalize value '{value}' for enum {enum_cls.__name__}")
    
class VistockMapper:
    @staticmethod
    def to_english_sector(vnsector: str) -> str:
        for sector in VistockSector:
            if sector.value == vnsector:
                return sector.name.replace('_', ' ').title()
            
        raise ValueError(f'No English mapping found for: {vnsector}')
        
class VistockGenerator:
    QUARTERS = ['03-31', '06-30', '09-30', '12-31']

    @staticmethod
    def generate_annual_dates(start_year: int, end_year: int) -> str:
        dates: List[str] = []

        for year in range(end_year, start_year - 1, -1):
            dates.append(f'{year}-12-31')

        return ','.join(dates)
    
    @staticmethod
    def generate_quarterly_dates(start_year: int, end_year: int) -> str:
        dates: List[str] = []

        for year in range(end_year, start_year - 1, -1):
            for q in reversed(VistockGenerator.QUARTERS):
                dates.append(f'{year}-{q}')

        return ','.join(dates)
    
    @staticmethod
    def generate_start_date(period: Union[VistockPeriodCode, str]) -> Optional[str]:
        if not VistockValidator.validate_enum_value(period, VistockPeriodCode):
            raise ValueError(
                f'Invalid period: "{period}". The period must be one of the predefined values: {", ".join([p.value for p in VistockPeriodCode])}. Please ensure that the period is specified correctly.'
            )
        period = VistockNormalizator.to_enum(period, VistockPeriodCode)
        
        today = datetime.now()

        match period:
            case VistockPeriodCode.ONE_DAY:
                start_date = today - relativedelta(days=1)
            case VistockPeriodCode.ONE_WEEK:
                start_date = today - relativedelta(weeks=1)
            case VistockPeriodCode.ONE_MONTH:
                start_date = today - relativedelta(months=1)
            case VistockPeriodCode.THREE_MONTHS:
                start_date = today - relativedelta(months=3)
            case VistockPeriodCode.SIX_MONTHS:
                start_date = today - relativedelta(months=6)
            case VistockPeriodCode.ONE_YEAR:
                start_date = today - relativedelta(years=1)
            case VistockPeriodCode.MONTH_TO_DATE:
                start_date = today.replace(day=1)
            case VistockPeriodCode.QUARTER_TO_DATE:
                start_date = today.replace(
                    month=((today.month - 1) // 3) * 3 + 1,
                    day=1
                )
            case VistockPeriodCode.YEAR_TO_DATE:
                start_date = today.replace(month=1, day=1)
            case VistockPeriodCode.ALL:
                return None
            case _:
                return None
            
        return start_date.strftime('%Y-%m-%d')
    
class VistockConverter:
    @staticmethod
    def from_utc_to_local(utc_time: str) -> str:
        try:
            utc_time_clean = utc_time.rstrip('Z')

            if '.' in utc_time_clean:
                date_part, ms_part = utc_time_clean.split('.')
                ms_part = (ms_part + '000000')[:6]
                utc_time_clean = f'{date_part}.{ms_part}'
                fmt = '%Y-%m-%dT%H:%M:%S.%f'
            else:
                fmt = '%Y-%m-%dT%H:%M:%S'

            utc_dt = datetime.strptime(utc_time_clean, fmt)
            utc_dt = utc_dt.replace(tzinfo=pytz.utc)

            local_tz = get_localzone()
            local_dt = utc_dt.astimezone(local_tz)

            return local_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        except Exception:
            return utc_time
        
    @staticmethod
    def from_date_to_timestamp(date: str) -> int:
        dt = datetime.strptime(date, '%Y-%m-%d')
        return int(time.mktime(dt.timetuple()))
    
    @staticmethod
    def from_timestamp_to_date(timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    @staticmethod
    def from_date_to_dateresolution(date: str, resolution: VistockResolutionCode) -> str:
        dt = datetime.strptime(date, '%Y-%m-%d')

        match resolution:
            case VistockResolutionCode.WEEK:
                return f'{dt.year}-W{dt.isocalendar().week:02d}'
            case VistockResolutionCode.MONTH:
                return f'{dt.year}-{dt.month:02d}'
            case VistockResolutionCode.YEAR:
                return f'{dt.year}'
            case _:
                return date
            

    