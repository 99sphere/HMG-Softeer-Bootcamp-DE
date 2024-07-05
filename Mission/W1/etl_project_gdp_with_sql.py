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

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
PATH = "assets/"
LOG_NAME = 'etl_project_log.txt'
JSON_NAME = "Countries_by_GDP.json"
REGION_INFO_NAME = "region_infos.json"

def logger(msg):
    with open(PATH+LOG_NAME, 'a') as f:
        time = datetime.now()
        time_str = f"{time.year}-{time.strftime("%B")}-{time.day:02d}-{time.hour:02d}-{time.second:02d}"
        f.write(time_str+', '+msg+'\n')
    return 
    
    
def extract():
    logger("Extracting Start.")
    
    # Get raw data
    response = requests.get(URL)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    raw_data = soup.select('table')

    # Transform raw data to pandas dataFrame
    table_df_list = pd.read_html(StringIO(str(raw_data)))
    tables_df = table_df_list[2]

    logger("Extracting Done")
    return raw_data

def transform(tables_df):
    logger("Transform Start.")
    
    # Transform raw data to pandas dataFrame
    table_df_list = pd.read_html(StringIO(str(tables_df)))
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
    with open("assets/region_infos.json", "r") as region_infos_json:
        continent_countries = json.load(region_infos_json)
        
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
    
    logger("Transform Done.")
    return data

def load(data, con):
    logger("Loading Start.")

    # Save in json file.
    data.to_json(PATH+JSON_NAME, orient='columns')
    
    # Save in sqlite3 DB
    data_sql = data[['Country/Territory', 'Forecast', 'Region']].copy().rename(columns={'Country/Territory':'Country', 'Forecast':'GDP_USD_billion'})
    data_sql.to_sql('Countries_by_GDP', con, if_exists='replace')   
    
    logger("Loading Done.")    
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
    tables_df = extract()
    data = transform(tables_df)
    load(data, con=con)
    
    # Requirements 1 (with SQL query)
    query = "SELECT Country FROM Countries_by_GDP WHERE GDP_USD_billion > 100"
    print(con.execute(query).fetchall())
    
    # Requirements 2 (with SQL query)
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion), 2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Asia' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion), 2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='North America' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion), 2) FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Europe' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion), 2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='South America' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion), 2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Africa' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())
    query = "SELECT Region, ROUND(AVG(GDP_USD_billion), 2)  FROM ( SELECT * FROM Countries_by_GDP  WHERE Region='Oceania' ORDER BY GDP_USD_billion DESC  LIMIT 5 )"
    print(con.execute(query).fetchall())