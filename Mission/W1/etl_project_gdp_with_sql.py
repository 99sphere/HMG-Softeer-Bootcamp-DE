import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os.path
from io import StringIO
import sqlite3 as sq3
import csv

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
    logger("Extracting Start.", log_fp)
    
    # Get raw data
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    raw_data = soup.select('table')

    logger("Extracting Done", log_fp)
        
    return raw_data

def transform(raw_data, log_fp):
    logger("Transform Start.", log_fp)
    
    # Transform raw data to pandas dataFrame
    table_df_list = pd.read_html(StringIO(str(raw_data)))
    tables_df = table_df_list[2]
    
    df_country = tables_df['Country/Territory'].copy()
    
    # Remove [%], and calc million to billion
    df_IMF_Year =  tables_df['IMF[1][13]']['Year'].copy()
    is_num = np.array((df_IMF_Year.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Year[idx]
        if len(orig_data) != 1:
            df_IMF_Year[idx] = orig_data[-4:]
        else:
            df_IMF_Year[idx] = np.nan

    # Remove [%], and calc million to billion
    df_IMF_Forecast =  tables_df['IMF[1][13]']['Forecast'].copy()
    is_num = np.array((df_IMF_Forecast.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Forecast[idx]
        if len(orig_data) == 1:
            df_IMF_Forecast[idx] = np.nan
    df_IMF_Forecast = (pd.to_numeric(df_IMF_Forecast) / 1000).round(2)

    # Concat transformed data
    data = pd.concat([df_country, df_IMF_Year, df_IMF_Forecast], axis=1)
    data = data.sort_values(by=['Forecast', "Country/Territory"], ascending=[False, True])

    # Add column for region info
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
    
    logger("Transform Done.", log_fp)
    return data

def load(data, log_fp, con):
    logger("Loading Start.", log_fp)

    # Save in json file.
    dir, _ = os.path.split(log_fp)
    json_fn = "Countries_by_GDP.json"
    json_fp = os.path.join(dir, json_fn)
    data.to_json(json_fp)
    
    # Save in sqlite3 DB
    data_sql = data[['Country/Territory', 'Forecast', 'Region']].copy().rename(columns={'Country/Territory':'Country', 'Forecast':'GDP_USD_billion'})
    data_sql.to_sql('Countries_by_GDP', con, if_exists='replace')   
    logger("Loading Done.", log_fp)    
    return 

if __name__=="__main__":
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    path = "assets/"
    filename = 'etl_project_log.txt'
    file_path = path + filename
    
    # con.close()
    con = sq3.connect('./assets/World_Economies.db')
    cursor = con.cursor()

    try:
        query = "CREATE TABLE Countries_by_GDP (Country text PRIMARY KEY, GDP_USD_billion float);"
        cursor.execute(query)
    except Exception as error:
        print(error)

    # init log file.
    if not os.path.isfile(file_path):
        f = open(file_path, 'w')
        f.close() 

    # Run ETL Process
    raw_data = extract(url, log_fp=file_path)
    data = transform(raw_data, log_fp=file_path)
    load(data, log_fp=file_path, con=con)
    
    # Requirements 1 (with SQL query)
    query = "SELECT Country FROM Countries_by_GDP WHERE GDP_USD_billion > 100"
    print(con.execute(query).fetchall())
    
    # Requirements 2 (with SQL query)
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion),2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Asia' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion),2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='North America' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion) 2) FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Europe' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion),2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='South America' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion),2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Africa' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion),2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Oceania' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())