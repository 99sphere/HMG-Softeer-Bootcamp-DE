import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os.path
from io import StringIO

def logger(msg, log_fp):
    with open(log_fp, 'a') as f:
        time = datetime.now()
        time_str = f"{time.year}-{time.strftime("%B")}-{time.day}-{time.hour}-{time.second}"
        f.write(time_str+', '+msg+'\n')
        
    return None
    
def extract(url, log_fp):
    """
    Extract GDP info from "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    and save into json file.
    """
    msg = "Extracting Start."
    logger(msg, log_fp)
    response = requests.get(url)
    html = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html, 'html.parser')
    # 현재 페이지에서 table 태그 모두 선택하기
    raw_data = soup.select('table')

    msg = "Extracting Done"
    logger(msg, log_fp)
        
    return raw_data

def transform(raw_data, log_fp):
    msg = "Transform Start."
    logger(msg, log_fp)
    
    table_df_list = pd.read_html(StringIO(str(raw_data)))
    tables_df = table_df_list[2]
    
    # Transform for "Country/Territory"
    df_country = tables_df['Country/Territory'].copy()
    
    # Transform for "Year"
    df_IMF_Year =  tables_df['IMF[1][13]']['Year'].copy()
    is_num = np.array((df_IMF_Year.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Year[idx]
        if len(orig_data) != 1:
            df_IMF_Year[idx] = orig_data[-4:]
        else:
            df_IMF_Year[idx] = np.nan

    # Transform for "Forecast"
    df_IMF_Forecast =  tables_df['IMF[1][13]']['Forecast'].copy()
    is_num = np.array((df_IMF_Forecast.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Forecast[idx]
        if len(orig_data) == 1:
            df_IMF_Forecast[idx] = np.nan
            
            
    df_IMF_Forecast = (pd.to_numeric(df_IMF_Forecast) / 1000).round(2)

    data = pd.concat([df_country, df_IMF_Year, df_IMF_Forecast], axis=1)
    data = data.sort_values(by=['Forecast', "Country/Territory"], ascending=[False, True])
    msg = "Transform Done."
    logger(msg, log_fp)
    return data

def load(data, log_fp):
    msg = "Loading Start."
    logger(msg, log_fp)

    dir, _ = os.path.split(log_fp)
    json_fn = "Countries_by_GDP.json"
    json_fp = os.path.join(dir, json_fn)
    data.to_json(json_fp)
    logger("Loading Done.", log_fp)
    return None

if __name__=="__main__":
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    path = "assets/"
    filename = 'etl_project_log.txt'
    file_path = path + filename
    
    if not os.path.isfile(file_path):
        f = open(file_path, 'w')
        f.close() 

    raw_data = extract(url, log_fp=file_path)
    data = transform(raw_data, log_fp=file_path)
    load(data, log_fp=file_path)
    
    # Requirements 1
    over_100B_GDP_nations = data.loc[data.Forecast > 100]['Country/Territory']
    over_100B_GDP_nations_list = list(over_100B_GDP_nations)
    print("[Requirements 1] Over 100B GDP\n ", *over_100B_GDP_nations_list, sep=' ')

    # Requirements 2
    # TODO Transform 안에서 region column 만들어주기
    continent_countries = {
        "Asia": ["East Timor", "Macau", "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen", "Hong Kong"],
        "North America": ["Turks and Caicos Islands", "Sint Maarten ", "Montserrat", "Greenland", "Curaçao", "Cayman Islands", "British Virgin Islands", "Bermuda", "Anguilla", "Puerto Rico", "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"],
        "Europe": ["Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kazakhstan", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom", "Vatican City"],
        "South America": ["Aruba", "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"],
        "Africa": ["Zanzibar", "São Tomé and Príncipe", "Cape Verde", "DR Congo", "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros", "Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
        "Oceania": ["New Caledonia", "French Polynesia", "Cook Islands", "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"]
    }
    
    all_nations_list = list(data['Country/Territory'])
    regions = []
    
    for nation in all_nations_list:
        for key, value in continent_countries.items():
            find=0
            if nation in value:
                regions.append(key)
                find=1
                break
        if not find:
            regions.append("None")

    data['Region']=regions
    
    region_names = ["Asia", "North America", "Europe", "South America", "Africa", "Oceania"]

    print("\n[Requirements 2] Average GDP of Top 5 Nations (Unit: Billion Dollars)")    
    for region_name in region_names:
        top5_avg_GDP = round(data.loc[data.Region==region_name].iloc[:5]['Forecast'].mean(), 2)
        print(f"{region_name}: {top5_avg_GDP}")