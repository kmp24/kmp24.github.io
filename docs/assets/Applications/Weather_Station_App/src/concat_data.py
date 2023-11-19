import pandas as pd
import glob

from constants import WX_DIR as wx_dir

def open_txt(filename):
    df = pd.read_csv(filename, sep='\t', header=None)
    df['station'] = filename.split('\\')[-1].replace('.txt','')
    return df

def concatenate_txt(wx_dir):
    # use glob to gather all the files in the wx_data directory
    wx_files = [f for f in glob.glob(wx_dir+'\*.txt')]
    wx_df = pd.concat([open_txt(f) for f in wx_files])
    wx_df.columns = ['date','max_temp_tenths_c','min_temp_tenths_c','precip_tenths_mm','station_id']

    # transform string date to datetime for db formatting
    wx_df['date'] = pd.to_datetime(wx_df.date, format='%Y%m%d')
    
    # Check for duplicate records based on date of observation and station ID
    # TODO add more checks/cleaning
    record_count = wx_df.groupby(['date', 'station_id'])['station_id'].transform('size')
    print(len(wx_df[record_count > 1]))
    
    return wx_df


wx_df = concatenate_txt(wx_dir)

# Write the data to csv for later use, or combine these steps in ingest_data.py
wx_df.to_csv('output_weather_station_data.csv', index=False)