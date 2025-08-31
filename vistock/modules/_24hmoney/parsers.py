from vistock.core.interfaces.ivistockparser import IVistockStockListingParser
from vistock.core.constants import DEFAULT_24HMONEY_LIMIT
from vistock.core.enums import (
    VistockIndustryCategory,
    VistockFloorCategory,
    VistockCompanyTypeCategory,
    VistockLetterCategory
)
from vistock.core.models import (
    StandardStockListingSearch,
    StandardStockListingSearchResults
)
from vistock.core.utils import (
    VistockValidator,
    VistockNormalizator
)
from typing import List, Dict, Union, Any

class Vistock24HMoneyStockListingParser(IVistockStockListingParser):
    def __init__(self):
        self._query = '?&industry_code={industry}&floor_code={floor}&com_type={company_type}&letter={letter}&page=1&per_page={limit}'

    def to_query(
        self,
        industry: Union[VistockIndustryCategory, str] = VistockIndustryCategory.ALL,
        floor: Union[VistockFloorCategory, str] = VistockFloorCategory.ALL,
        company_type: Union[VistockCompanyTypeCategory, str] = VistockCompanyTypeCategory.ALL,
        letter: Union[VistockLetterCategory, str] = VistockLetterCategory.ALL
    ) -> str:
        if not VistockValidator.validate_enum_value(industry, VistockIndustryCategory):
            raise ValueError(
                f'Invalid industry: "{industry}". The industry must be one of the predefined values: {", ".join([r.value for r in VistockIndustryCategory])}. Please ensure that the industry is specified correctly.'
            )
        industry = VistockNormalizator.to_enum(industry, VistockIndustryCategory)

        if not VistockValidator.validate_enum_value(floor, VistockFloorCategory):
            raise ValueError(
                f'Invalid floor: "{floor}". The floor must be one of the predefined values: {", ".join([r.value for r in VistockFloorCategory])}. Please ensure that the floor is specified correctly.'
            )
        floor = VistockNormalizator.to_enum(floor, VistockFloorCategory)

        if not VistockValidator.validate_enum_value(company_type, VistockCompanyTypeCategory):
            raise ValueError(
                f'Invalid company type: "{company_type}". The company type must be one of the predefined values: {", ".join([r.value for r in VistockCompanyTypeCategory])}. Please ensure that the company type is specified correctly.'
            )
        company_type = VistockNormalizator.to_enum(company_type, VistockCompanyTypeCategory)

        if not VistockValidator.validate_enum_value(letter, VistockLetterCategory):
            raise ValueError(
                f'Invalid letter: "{letter}". The letter must be one of the predefined values: {", ".join([r.value for r in VistockLetterCategory])}. Please ensure that the letter is specified correctly.'
            )
        letter = VistockNormalizator.to_enum(letter, VistockLetterCategory)

        return self._query.format(
            industry=VistockNormalizator.to_string(industry, VistockIndustryCategory).lower(),
            floor = VistockNormalizator.to_string(floor, VistockFloorCategory).lower(),
            company_type = VistockNormalizator.to_string(company_type, VistockCompanyTypeCategory).lower(),
            letter = VistockNormalizator.to_string(letter, VistockLetterCategory).lower(),
            limit=DEFAULT_24HMONEY_LIMIT
        )
    
    def to_standard(
        self,
        data: List[Dict[str, Any]]
    ) -> StandardStockListingSearchResults:
        return StandardStockListingSearchResults(
        results=[
            StandardStockListingSearch(
                code=item.get('symbol', ''),
                company_name=item.get('company_name', ''),
                tfloor=item.get('floor', ''),
                company_type=item.get('fiingroup_com_type_code', ''),
                icb_name_vi=item.get('icb_name_vi', ''),
                listed_share_vol=item.get('listed_share_vol', 0),
                fiingroup_icb_code=item.get('fiingroup_icb_code', 0)
            )
            for item in data
        ],
        total_results=len(data)
    )
