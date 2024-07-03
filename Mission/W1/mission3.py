import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os.path

def extract(url, log_fp):
    f = open(log_fp, 'a')
    # time = datetime.now()
    # time_str = f"{time.year}-{time.strftime("%B")}-{time.day}-{time.hour}-{time.second}"
    # breakpoint()
    f.write()
    """
    Extract GDP info from "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    and save into json file.
    """
    response = requests.get(url)
    html = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html, 'html.parser')
    # 현재 페이지에서 table 태그 모두 선택하기
    raw_data = soup.select('table')
    
    f.close() 

    return raw_data

def transform(raw_data, log_fp):
    f = open(log_fp, 'a')

    table_df_list = pd.read_html(str(raw_data))
    tables_df = table_df_list[2]
    
    # Transform for "Country/Territory"
    df_country = tables_df['Country/Territory']
    
    # Transform for "Year"
    df_IMF_Year =  tables_df['IMF[1][13]']['Year']
    is_num = np.array((df_IMF_Year.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Year[idx]
        if len(orig_data) != 1:
            df_IMF_Year[idx] = orig_data[-4:]
        else:
            df_IMF_Year[idx] = np.nan

    # Transform for "Forecast"
    df_IMF_Forecast =  tables_df['IMF[1][13]']['Forecast']    
    is_num = np.array((df_IMF_Forecast.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Forecast[idx]
        if len(orig_data) == 1:
            df_IMF_Forecast[idx] = np.nan
            
            
    df_IMF_Forecast = (pd.to_numeric(df_IMF_Forecast) / 1000).round(2)

    data = pd.concat([df_country, df_IMF_Year, df_IMF_Forecast], axis=1)
    f.close() 

    return data

def load(data, log_fp):
    f = open(log_fp, 'a')

    data = OrderedDict()

    # TBD    
    f.close() 
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
    