from data_model import StationStats
import pandas as pd
from constants import DATABASE_URI, WEATHER_STATION_TABLE, STATION_STATS_TABLE
from sqlalchemy import create_engine
from ingest_data import load_data
import numpy as np
from functools import reduce

def db_table_to_df(table_name, database_connection):
    # pull all the data from database into a pandas dataframe for analysis
    df = pd.read_sql(f"SELECT * FROM {WEATHER_STATION_TABLE}", database_connection)
    return df


def fill_df_na(df):
    df = df.replace(-9999, np.nan)
    return df
engine = create_engine(DATABASE_URI)

def get_station_year_mean(df, field):
    df = df.groupby(['station_id','year'], dropna=True)[field].agg('mean').reset_index()
    df = df[['station_id','year',field]]
    df.columns = ['station_id','year',field.replace('_temp','_mean')]
    return df

def get_station_year_total(df, field):
    df = df.groupby(['station_id','year'], dropna=True)[field].agg('sum').reset_index()
    df = df[['station_id','year',field]]
    df.columns = ['station_id','year',field + '_total']
    return df

def convert_tenths(df, column_name):
    # Convert mm to cm
    if 'tenths_mm' in column_name:
        df[column_name.replace('_tenths_mm','_cm')] = df[column_name] / 100
        df.drop(column_name, inplace=True, axis=1)
        
    if 'tenths_c' in column_name:
        # Convert to degrees celsius
        df[column_name.replace('_tenths_c','_c')] = df[column_name] / 10
        df.drop(column_name, inplace=True, axis=1)
    return df

def concat_df_stats(df, min_field, max_field, precip_field):
    # Add a year field for grouping by station/year
    df['year'] = pd.to_datetime(df['date']).dt.year
    
    # Calculate the mean/max/total values
    max_mean =  get_station_year_mean(df, max_field)
    min_mean =  get_station_year_mean(df, min_field)
    total_precip = get_station_year_total(df,  precip_field)
    
    # Merge the dataframes based on station id into one dataframe
    df_list = [max_mean, min_mean, total_precip]
    merged = reduce(lambda l, r: pd.merge(l, r, on=['station_id','year'], how='outer'), df_list)
    
    # Convert to the desired units
    for col in merged.columns:
        merged = convert_tenths(merged, col)
    
    return merged
    


# Open the weather_station table and load the data for the analysis
with engine.connect() as connection:  
    df = db_table_to_df(WEATHER_STATION_TABLE, connection)
    df = fill_df_na(df)
    stats_df = concat_df_stats(df, 'min_temp_tenths_c','max_temp_tenths_c', 'precip_tenths_mm')

    # Load the data into the stations table (station_id, year, and mean/total stats)
    load_data(stats_df, connection, STATION_STATS_TABLE)