import os
import openpyxl
import ujson

def create_TB_countries(version):
    
    xlsx = openpyxl.load_workbook(
                '.\Tools\DefaultDataManager\TB\ModData\WHO_TB_CountryData2022.xlsx', read_only=False, keep_vba=False, data_only=False, keep_links=True)

    countries = {}
    for row in range(2, xlsx['Countries'].max_row+1):
        row_str = str(row)
        country = {
            'name': xlsx['Countries']['A'+row_str].value,
            'ISO2': xlsx['Countries']['B'+row_str].value,
            'ISO3': xlsx['Countries']['C'+row_str].value,
            'ISONumeric': xlsx['Countries']['D'+row_str].value,
        }
        countries[country['ISO3']] = country

    TB_Path = os.getcwd()+'\Tools\DefaultDataManager\TB\\'
    #os.makedirs(TB_Path+'\JSON\countries\\', exist_ok=True)
    with open(TB_Path+'\JSON\countries.JSON', 'w') as f:
        ujson.dump(countries, f)
    #log(countries)