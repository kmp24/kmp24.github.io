from data_model import WeatherData
import pandas as pd
from constants import DATABASE_URI, WEATHER_STATION_TABLE
from sqlalchemy import create_engine
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

engine = create_engine(DATABASE_URI)

def load_data(df, db_connection, table):
    # Use the database connection to load the concatenated weather station data into the desired table
    df.to_sql(table, db_connection, if_exists='append', index=False)

# Open the weathern_station table and load the data
with engine.connect() as connection:  
    wx_df = pd.read_csv(r'output_weather_station_data.csv')  
    
    logging.info("Loading data to the weather_station table at %s", datetime.now())
    load_data(wx_df, engine.connect(), WEATHER_STATION_TABLE)
    logging.info("Loaded %s records to the weather_station table at %s", len(wx_df), datetime.now())

    # Check the loaded data
    df_check = pd.read_sql("SELECT * FROM weather_stations", connection)

    print(df_check.head())
