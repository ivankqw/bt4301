# tablebuilder.singstat.gov.sg/api/table/tabledata/{resourceId}
import requests
import pandas as pd 
from airflow.decorators import task

def get_cpi():
    urlData = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/M212881"
    headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'tablebuilder.singstat.gov.sg',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }
    res = requests.get(urlData, headers=headers)
    result = res.json()
    result = result['Data']

    key_value_pairs = result['row'][0]['columns']
    # turn into a dataframe
    df = pd.DataFrame(key_value_pairs)
    # rename columns 
    df.columns = ['year_month', 'Value']
    # convert to datetime
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y %b')
    # rename columns
    df.columns = ['Month', 'Value']
    return df

@task
def extract_cpi_task():
    print("Getting Singstat data...")
    data_path = "/opt/airflow/dags/data"
    df_cpi = get_cpi()
    data_path_cpi = data_path + "/cpi.csv"
    df_cpi.to_csv(data_path_cpi, index=False)
    print("Singstat data obtained.")
    return data_path_cpi