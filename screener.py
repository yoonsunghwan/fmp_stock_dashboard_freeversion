import requests
import fmpsdk

sector =\
    ['All','Communication Services', 'Energy', 'Technology', \
              'Industrials', 'Financial Services', 'Basic Materials', \
              'Consumer Cyclical', 'Consumer Defensive', 'Healthcare', \
              'Real Estate', 'Utilities', 'Financial', 'Building', \
              'Industrial Goods', 'Pharmaceuticals', 'Services', 'Conglomerates', \
              'Media', 'Banking', 'Airlines', 'Retail', 'Metals & Mining', 'Textiles', \
              'Apparel & Luxury Goods', 'Chemicals', 'Biotechnology', 'Electrical Equipment', \
              'Aerospace & Defense', 'Telecommunication', 'Machinery', 'Food Products', 'Insurance', \
              'Logistics & Transportation', 'Health Care', 'Beverages', 'Consumer products', \
              'Semiconductors', 'Automobiles', 'Trading Companies & Distributors', \
              'Commercial Services & Supplies', 'Construction', 'Auto Components', \
              'Hotels', 'Restaurants & Leisure', 'Life Sciences Tools & Services', \
              'Communications', 'Industrial Conglomerates', 'Professional Services', \
              'Road & Rail', 'Tobacco', 'Paper & Forest', 'Packaging', 'Leisure Products', \
              'Transportation Infrastructure', 'Distributors', 'Marine', 'Diversified Consumer Services']

industry = ['All','Entertainment', 'Oil & Gas Midstream', 'Semiconductors', 'Specialty Industrial Machinery',
            'Banks Diversified', 'Consumer Electronics', 'Software Infrastructure', 'Broadcasting', 'Computer Hardware',
            'Building Materials', 'Resorts & Casinos', 'Auto Manufacturers', 'Internet Content & Information',
            'Insurance Diversified', 'Telecom Services', 'Metals & Mining', 'Capital Markets', 'Steel',
            'Footwear & Accessories', 'Household & Personal Products', 'Other Industrial Metals & Mining',
            'Oil & Gas E&P', 'Banks Regional', 'Drug Manufacturers General', 'Internet Retail',
            'Communication Equipment', 'Semiconductor Equipment & Materials', 'Oil & Gas Services',
            'Chemicals', 'Electronic Gaming & Multimedia', 'Oil & Gas Integrated', 'Credit Services',
            'Online Media', 'Business Services', 'Biotechnology', 'Grocery Stores', 'Oil & Gas Equipment & Services',
            'REITs', 'Copper', 'Software Application', 'Home Improvement Retail', 'Pharmaceutical Retailers',
            'Communication Services', 'Oil & Gas Drilling', 'Electronic Components', 'Packaged Foods',
            'Information Technology Services', 'Leisure', 'Specialty Retail', 'Oil & Gas Refining & Marketing',
            'Tobacco', 'Financial Data & Stock Exchanges', 'Insurance Specialty', 'Beverages Non-Alcoholic',
            'Asset Management', 'REIT Diversified', 'Residential Construction', 'Travel & Leisure', 'Gold',
            'Discount Stores', 'Confectioners', 'Medical Devices', 'Banks', 'Independent Oil & Gas', 'Airlines',
            'Travel Services', 'Aerospace & Defense', 'Retail Apparel & Specialty', 'Diagnostics & Research',
            'Trucking', 'Insurance Property & Casualty', 'Health Care Plans', 'Consulting Services', 'Aluminum',
            'Beverages Brewers', 'REIT Residential', 'Education & Training Services', 'Apparel Retail', 'Railroads',
            'Apparel Manufacturing', 'Staffing & Employment Services', 'Utilities Diversified', 'Agricultural Inputs',
            'Restaurants', 'Drug Manufacturers General Specialty & Generic', 'Financial Conglomerates',
            'Personal Services', 'Thermal Coal', 'REIT Office', 'Advertising Agencies', 'Farm & Heavy Construction Machinery',
            'Consumer Packaged Goods', 'Publishing', 'Specialty Chemicals', 'Engineering & Construction',
            'Utilities Independent Power Producers', 'Utilities Regulated Electric', 'Medical Instruments & Supplies',
            'Building Products & Equipment', 'Packaging & Containers', 'REIT Mortgage', 'Department Stores',
            'Insurance Life', 'Luxury Goods', 'Auto Parts', 'Autos', 'REIT Specialty', 'Integrated Freight & Logistics',
            'Security & Protection Services', 'Utilities Regulated Gas', 'Airports & Air Services', 'Farm Products',
            'REIT Healthcare Facilities', 'REIT Industrial', 'Metal Fabrication', 'Scientific & Technical Instruments',
            'Solar', 'REIT Hotel & Motel', 'Medical Distribution', 'Medical Care Facilities', 'Agriculture',
            'Food Distribution', 'Health Information Services', 'Industrial Products', 'REIT Retail', 'Conglomerates',
            'Health Care Providers', 'Waste Management', 'Beverages Wineries & Distilleries', 'Marine Shipping',
            'Real Estate Services', 'Tools & Accessories', 'Auto & Truck Dealerships', 'Industrial Distribution',
            'Uranium', 'Lodging', 'Electrical Equipment & Parts', 'Gambling', 'Specialty Business Services',
            'Recreational Vehicles', 'Furnishings', 'Fixtures & Appliances', 'Forest Products', 'Silver',
            'Business Equipment & Supplies', 'Medical Instruments & Equipment', 'Utilities Regulated', 'Coking Coal',
            'Insurance Brokers', 'Rental & Leasing Services', 'Lumber & Wood Production', 'Medical Diagnostics & Research',
            'Pollution & Treatment Controls', 'Transportation & Logistics', 'Other Precious Metals & Mining',
            'Brokers & Exchanges', 'Beverages Alcoholic', 'Mortgage Finance', 'Utilities Regulated Water',
            'Manufacturing Apparel & Furniture', 'Retail Defensive', 'Real Estate Development', 'Paper & Paper Products',
            'Insurance Reinsurance', 'Homebuilding & Construction', 'Coal', 'Electronics & Computer Distribution',
            'Health Care Equipment & Services', 'Education', 'Employment Services', 'Textile Manufacturing',
            'Real Estate Diversified', 'Consulting & Outsourcing', 'Utilities Renewable', 'Tobacco Products',
            'Farm & Construction Machinery', 'Shell Companies', 'N/A', 'Advertising & Marketing Services',
            'Capital Goods', 'Insurance', 'Industrial Electrical Equipment', 'Utilities', 'Pharmaceuticals',
            'Biotechnology & Life Sciences', 'Infrastructure Operations', 'Energy', 'NULL', 'Property Management',
            'Auto Dealerships', 'Apparel Stores', 'Mortgage Investment', 'Software & Services', 'Industrial Metals & Minerals',
            'Media & Entertainment', 'Diversified Financials', 'Consumer Services', 'Commercial  & Professional Services',
            'Electronics Wholesale', 'Retailing', 'Automobiles & Components', 'Materials', 'Real Estate', 'Food',
            'Beverage & Tobacco', 'Closed-End Fund Debt', 'Transportation',
            'Food & Staples Retailing', 'Consumer Durables & Apparel', 'Technology Hardware & Equipment',
            'Telecommunication Services', 'Semiconductors & Semiconductor Equipment']


exchange = ['ETF', 'MUTUAL_FUND', 'COMMODITY', 'INDEX', 'CRYPTO', 'FOREX', 'TSX', 'AMEX', 'NASDAQ', 'NYSE', 'EURONEXT']
