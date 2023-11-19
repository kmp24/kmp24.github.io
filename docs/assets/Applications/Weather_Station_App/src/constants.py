import os
WEATHER_STATION_TABLE = 'weather_stations'
STATION_STATS_TABLE = 'station_stat'
DATABASE_URI = 'sqlite:///weather_data.db'

dirname = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
WX_DIR  = os.path.join(dirname, 'wx_data')