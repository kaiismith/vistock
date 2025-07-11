from enum import Enum

class Vistock24HMoneyIndustryCategory(Enum):
    OIL_AND_GAS = '0500'
    CHEMICALS = '1300'
    BASIC_RESOURCES = '1700'
    CONSTRUCTION_AND_MATERIALS = '2300'
    INDUSTRIAL_GOODS_AND_SERVICES = '2700'
    AUTOMOBILES_AND_PARTS = '3300'
    FOOD_AND_BEVERAGE = '3500'
    PERSONAL_HOUSEHOLD_GOODS = '3700'
    HEALTH_CARE = '4500'
    RETAIL = '5300'
    MEDIA = '5500'
    TRAVEL_AND_LEISURE = '5700'
    TELECOMMUNICATIONS = '6500'
    ULTILITIES = '7500' # Electrticity, Water, Fuel & Gas
    BANKS = '8300'
    INSURANCE = '8500'
    REAL_ESTATE = '8600'
    FINANCIAL_SERVICES = '8700'
    INFORMATION_TECHNOLOGY = '9500'
    ALL = 'all'

class Vistock24HMoneyFloorCategory(Enum):
    HOSE = 'HOSE'
    HNX = 'HNX'
    UPCOM = 'UPCOM'
    ALL = 'all'

class Vistock24HMoneyCompanyCategory(Enum):
    COMMON_TECHNOLOGY_SHARES = 'CT'
    BANKING = 'NH'
    INSURANCE = 'BH'
    SECURITIES = 'CK'
    INVESTMENT_FUND = 'FUND'
    ALL = 'all'

class Vistock24HMoneyLetterCategory(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    M = 'M'
    N = 'N'
    O = 'O'
    P = 'P'
    Q = 'Q'
    R = 'R'
    S = 'S'
    T = 'T'
    U = 'U'
    V = 'V'
    W = 'W'
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    ALL = 'all'

class Vistock24HMoneySectionMapping(Enum):
    APPAREL_RETAIL = 'Bán lẻ hàng may mặc'
    COMPLEX_RETAIL = 'Bán lẻ phức hợp'
    LIFE_INSURANCE = 'Bảo hiểm nhân thọ'
    NON_LIFE_INSURANCE = 'Bảo hiểm phi nhân thọ'
    REAL_ESTATE = 'Bất động sản'
    EXPRESS_DELIVERY = 'Chuyển phát nhanh'
    HEALTHCARE = 'Chăm sóc y tế'
    WASTE_ENVIRONMENT = 'Chất thải & Môi trường'
    CONTAINERS_PACKAGING = 'Containers & Đóng gói'
    COMPLEX_INDUSTRIES = 'Công nghiệp phức hợp'
    BIOTECHNOLOGY = 'Công nghệ sinh học'
    PHARMACEUTICALS = 'Dược phẩm'
    COMPUTER_SERVICES = 'Dịch vụ Máy tính'
    ENTERTAINMENT_SERVICES = 'Dịch vụ giải trí'
    SPECIALTY_CONSUMER_SERVICES = 'Dịch vụ tiêu dùng chuyên ngành'
    MEDIA_SERVICES = 'Dịch vụ truyền thông'
    TRANSPORTATION_SERVICES = 'Dịch vụ vận tải'
    MEDICAL_INSTRUMENTS = 'Dụng cụ y tế'
    ENTERTAINMENT_MEDIA = 'Giải trí & Truyền thông'
    FOOTWEAR = 'Giầy dép'
    APPAREL = 'Hàng May mặc'
    PERSONAL_GOODS = 'Hàng cá nhân'
    AVIATION = 'Hàng không'
    ELECTRICAL_ELECTRONICS = 'Hàng điện & điện tử'
    INTERNET = 'Internet'
    MINING = 'Khai khoáng '
    COAL_MINING = 'Khai thác Than'
    GOLD_MINING = 'Khai thác vàng'
    LOGISTICS = 'Kho bãi, hậu cần và bảo dưỡng'
    HOTELS = 'Khách sạn'
    NON_FERROUS_METALS = 'Kim Loại màu'
    TIMBER_WOOD = 'Lâm sản và Chế biến gỗ'
    TIRES = 'Lốp xe'
    INDUSTRIAL_MACHINERY = 'Máy công nghiệp'
    SECURITIES_BROKERAGE = 'Môi giới chứng khoán'
    BANKING = 'Ngân hàng'
    EQUIPMENT_SUPPLIERS = 'Nhà cung cấp thiết bị'
    RESTAURANTS_BARS = 'Nhà hàng và quán bar'
    ALUMINUM = 'Nhôm'
    PLASTICS_RUBBER_FIBERS = 'Nhựa, cao su & sợi'
    AGRICULTURE_AQUACULTURE = 'Nuôi trồng nông & hải sản'
    WATER = 'Nước'
    PHARMA_DISTRIBUTION = 'Phân phối dược phẩm'
    SPECIALTY_DISTRIBUTION = 'Phân phối hàng chuyên dụng'
    FOOD_DISTRIBUTION = 'Phân phối thực phẩm'
    FUEL_GAS_DISTRIBUTION = 'Phân phối xăng dầu & khí đốt'
    HARDWARE = 'Phần cứng'
    SOFTWARE = 'Phần mềm'
    AUTO_PARTS = 'Phụ tùng ô tô'
    ASSET_MANAGEMENT = 'Quản lý tài sản'
    INVESTMENT_FUNDS = 'Quỹ đầu tư'
    BOOKS_CULTURE = 'Sách, ấn bản & sản phẩm văn hóa'
    CHEMICALS = 'Sản phẩm hóa dầu, Nông dược & Hóa chất khác'
    ELECTRICITY = 'Sản xuất & Phân phối Điện'
    BEER_PRODUCTION = 'Sản xuất bia '
    PAPER_PRODUCTION = 'Sản xuất giấy'
    OIL_GAS = 'Sản xuất và Khai thác dầu khí'
    AUTOMOBILE_MANUFACTURING = 'Sản xuất ô tô'
    HOME_APPLIANCES = 'Thiết bị gia dụng'
    TELECOM_EQUIPMENT = 'Thiết bị viễn thông'
    OIL_GAS_EQUIP_SERVICES = 'Thiết bị và Dịch vụ Dầu khí'
    OFFICE_EQUIPMENT = 'Thiết bị văn phòng'
    MEDICAL_EQUIPMENT = 'Thiết bị y tế'
    ELECTRICAL_EQUIPMENT = 'Thiết bị điện'
    TOBACCO = 'Thuốc lá'
    STEEL_PRODUCTS = 'Thép và sản phẩm thép'
    FOOD = 'Thực phẩm'
    OTHER_UTILITIES = 'Tiện ích khác'
    PERSONAL_FINANCE = 'Tài chính cá nhân'
    SPECIAL_FINANCE = 'Tài chính đặc biệt'
    REINSURANCE = 'Tái bảo hiểm'
    REAL_ESTATE_CONSULTING = 'Tư Vấn, Định giá, Môi giới Bất động sản'
    BUSINESS_CONSULTING = 'Tư vấn & Hỗ trợ KD'
    WINE_SPIRITS = 'Vang & Rượu mạnh'
    FIXED_TELECOM = 'Viễn thông cố định'
    MOBILE_TELECOM = 'Viễn thông di động'
    WATER_TRANSPORT = 'Vận tải Thủy'
    PASSENGER_TRAVEL = 'Vận tải hành khách & Du lịch'
    BUILDING_MATERIALS = 'Vật liệu xây dựng & Nội thất'
    TRUCKS_SHIPBUILDING = 'Xe tải & Đóng tàu'
    CONSTRUCTION = 'Xây dựng'
    CONSUMER_ELECTRONICS = 'Điện tử tiêu dùng'
    TRAINING_EMPLOYMENT = 'Đào tạo & Việc làm'
    TOYS = 'Đồ chơi'
    DURABLE_HOUSEHOLD_GOODS = 'Đồ gia dụng lâu bền'
    DISPOSABLE_HOUSEHOLD_GOODS = 'Đồ gia dụng một lần'
    BEVERAGES_REFRESHMENTS = 'Đồ uống & giải khát'

class VistockVnDirectFinancialModelsCategory(Enum):
    BALANCE_SHEET = '1,89,101,411'
    INCOME_STATEMENT = '2,90,102,412'
    CASH_FLOW_STATEMENT = '3,91,103,413'
    ALL = 'all'

class VistockVnDirectReportTypeCategory(Enum):
    ANNUAL = 'ANNUAL'
    QUARTER = 'QUARTER'

# class VistockVnDirectFiscalDateCategory(Enum):
#     ANNUAL = '2025-12-31,2024-12-31,2023-12-31,2022-12-31,2021-12-31,2020-12-31,2019-12-31,2018-12-31,2017-12-31,2016-12-31'
#     SPRING = '2025-03-31,2024-12-31,2024-09-30,2024-06-30,2024-03-31,2023-12-31,2023-09-30,2023-06-30,2023-03-31,2022-12-31'
#     SUMMER = '2025-06-30,2025-03-31,2024-12-31,2024-09-30,2024-06-30,2024-03-31,2023-12-31,2023-09-30,2023-06-30,2023-03-31'
#     AUTUMN = '2025-09-30,2025-06-30,2025-03-31,2024-12-31,2024-09-30,2024-06-30,2024-03-31,2023-12-31,2023-09-30,2023-06-30'
#     WINTER = '2025-12-31,2025-09-30,2025-06-30,2025-03-31,2024-12-31,2024-09-30,2024-06-30,2024-03-31,2023-12-31,2023-09-30'
